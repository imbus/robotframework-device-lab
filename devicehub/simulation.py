"""Simuliertes Messmodul MM-100: Zustände, Register, Messungen und Fehler-Injektion.

Die Zustände werden bei jedem Zugriff aus Zeitstempeln fortgeschrieben. So braucht die
Simulation keine Hintergrund-Threads und bleibt nachvollziehbar.

Das Register `setpoint_voltage` bildet die Spannungsquelle am Messeingang nach: Das Gerät
misst, was dort anliegt (plus Rauschen).

    OFF → BOOTING → SETTLING → READY → MEASURING → READY,  dazu FAULT
"""

import os
import random
import time
from dataclasses import dataclass
from enum import StrEnum
from typing import Literal


class State(StrEnum):
    OFF = "OFF"
    BOOTING = "BOOTING"
    SETTLING = "SETTLING"
    READY = "READY"
    MEASURING = "MEASURING"
    FAULT = "FAULT"


# Inhalt des Statusregisters je Zustand
STATUS_CODES = {
    State.OFF: 0,
    State.BOOTING: 1,
    State.SETTLING: 2,
    State.READY: 3,
    State.MEASURING: 4,
    State.FAULT: 9,
}

Fault = Literal["hang", "drift", "disconnect"]

# Realistische Dauern in Sekunden; die Simulation multipliziert sie mit SIM_TIME_SCALE.
# Die Demo läuft mit Faktor 0.1 (READY nach ca. 5 s); darauf sind die Timeouts in den
# Testdaten (15 s) abgestimmt.
BOOT_S = 20.0
POWER_ON_SETTLE_S = 30.0
SETPOINT_SETTLE_S = 10.0
SAMPLE_S = 2.0

# Bei Fehler "drift" weicht jeder weitere Messwert um 0,7 % der Eingangsspannung mehr ab.
DRIFT_PER_SAMPLE = 0.007


class SimulationError(Exception):
    """Die Anfrage passt nicht zum Gerät oder zu seinem Zustand."""

    def __init__(self, message: str, status_code: int = 409) -> None:
        super().__init__(message)
        self.status_code = status_code


@dataclass(frozen=True)
class DeviceSpec:
    """Feste Eigenschaften eines simulierten Geräts."""

    device_id: str
    model: str
    variant: str
    serial_number: str
    firmware_version: str
    max_voltage_v: float
    registers: dict[str, int]  # Name → Adresse


DEVICE_SPECS = (
    DeviceSpec(
        device_id="mm100-a",
        model="MM-100",
        variant="A",
        serial_number="MM100A-2026-0417",
        firmware_version="2.4.1",
        max_voltage_v=30.0,
        registers={
            "setpoint_voltage": 40001,
            "measured_voltage": 30001,
            "temperature": 30003,
            "status": 30010,
        },
    ),
    DeviceSpec(
        device_id="mm100-b",
        model="MM-100",
        variant="B",
        serial_number="MM100B-2026-1138",
        firmware_version="3.0.2",
        max_voltage_v=250.0,
        registers={
            "setpoint_voltage": 41001,
            "measured_voltage": 31001,
            "temperature": 31003,
            "status": 31010,
        },
    ),
    # Variante C hat noch kein Geräteprofil: Demo „Neues Gerät in 60 Sekunden“
    DeviceSpec(
        device_id="mm100-c",
        model="MM-100",
        variant="C",
        serial_number="MM100C-2026-0052",
        firmware_version="3.1.0",
        max_voltage_v=250.0,
        registers={
            "setpoint_voltage": 42001,
            "measured_voltage": 32001,
            "temperature": 32003,
            "status": 32010,
        },
    ),
)


class Device:
    """Ein simuliertes Messgerät."""

    def __init__(self, spec: DeviceSpec, sim: Simulation) -> None:
        self.spec = spec
        self._sim = sim
        self._state = State.OFF
        self._phase_end: float | None = None  # Zeitpunkt, an dem der Zustand von selbst wechselt
        self.setpoint_voltage_v = 0.0
        self._measurement: list[dict[str, float]] | None = None  # Werte der letzten Messung
        self._drift_samples = 0
        # Getrennte Zufallsquellen: Lesezugriffe der Web-Seite verändern keine Messergebnisse.
        self._measurement_rng = random.Random()
        self._live_rng = random.Random()

    @property
    def state(self) -> State:
        self._advance()
        return self._state

    def info(self) -> dict:
        state = self.state
        measured_v = (
            self._sample(self._live_rng)["voltage_v"]
            if state in (State.READY, State.MEASURING)
            else None
        )
        return {
            "id": self.spec.device_id,
            "model": self.spec.model,
            "variant": self.spec.variant,
            "serial_number": self.spec.serial_number,
            "firmware_version": self.spec.firmware_version,
            "state": state,
            "measured_voltage_v": measured_v,
        }

    def power(self, on: bool) -> None:
        if not on:
            self.reset()
            return
        state = self.state
        if state is State.FAULT:
            raise SimulationError(f"{self.spec.device_id} ist in FAULT – erst zurücksetzen")
        if state is State.OFF:
            # Bei jedem Einschalten neu säen: gleiche Messwerte bei jedem Testlauf.
            seed = f"{self._sim.seed}:{self.spec.device_id}"
            self._measurement_rng.seed(seed)
            self._live_rng.seed(f"{seed}:live")
            self._drift_samples = 0
            self._enter(State.BOOTING, time.monotonic(), BOOT_S)

    def reset(self) -> None:
        """Sicherer Zustand: aus, Eingangsspannung 0 V, keine Messung."""
        self._enter(State.OFF, time.monotonic())
        self.setpoint_voltage_v = 0.0
        self._measurement = None

    def read_register(self, address: int) -> float:
        name = self._register_name(address)
        state = self.state
        if state is State.OFF:
            raise SimulationError(
                f"{self.spec.device_id} ist ausgeschaltet – Register {address} nicht lesbar"
            )
        match name:
            case "setpoint_voltage":
                return self.setpoint_voltage_v
            case "measured_voltage":
                return self._sample(self._live_rng)["voltage_v"]
            case "temperature":
                return self._sample(self._live_rng)["temperature_c"]
            case _:  # status
                return STATUS_CODES[state]

    def write_register(self, address: int, value: float) -> None:
        name = self._register_name(address)
        if name != "setpoint_voltage":
            raise SimulationError(f"Register {address} ({name}) ist schreibgeschützt")
        state = self.state
        if state is not State.READY:
            raise SimulationError(
                f"{self.spec.device_id} nimmt nur in READY eine Eingangsspannung an, "
                f"nicht in {state}"
            )
        self.setpoint_voltage_v = value
        if value > self.spec.max_voltage_v:
            self._enter(State.FAULT, time.monotonic())  # Überspannungsschutz löst aus
        else:
            self._enter(State.SETTLING, time.monotonic(), SETPOINT_SETTLE_S)

    def start_measurement(self, repetitions: int) -> None:
        state = self.state
        if state is not State.READY:
            raise SimulationError(
                f"{self.spec.device_id} kann nur im Zustand READY messen, nicht in {state}"
            )
        self._measurement = [
            self._sample(self._measurement_rng, count_drift=True) for _ in range(repetitions)
        ]
        self._enter(State.MEASURING, time.monotonic(), SAMPLE_S * repetitions)

    def measurement_result(self) -> dict:
        if self._measurement is None:
            raise SimulationError(f"{self.spec.device_id} hat noch keine Messung gestartet", 404)
        done = self.state is not State.MEASURING  # fertig, sobald das Gerät nicht mehr misst
        return {"done": done, "values": self._measurement if done else []}

    def _enter(self, state: State, start: float, duration_s: float | None = None) -> None:
        self._state = state
        self._phase_end = None if duration_s is None else start + duration_s * self._sim.time_scale

    def _advance(self) -> None:
        """Schreibt den Zustand bis jetzt fort; jeder Zustand beginnt, wo der vorige endete."""
        now = time.monotonic()
        while self._phase_end is not None and now >= self._phase_end:
            ended_at = self._phase_end
            match self._state:
                case State.BOOTING:
                    self._enter(State.SETTLING, ended_at, POWER_ON_SETTLE_S)
                case State.SETTLING if self._sim.has_fault("hang"):
                    break  # bleibt in SETTLING, bis der Fehler gelöscht ist
                case State.SETTLING | State.MEASURING:
                    self._enter(State.READY, ended_at)

    def _sample(self, rng: random.Random, count_drift: bool = False) -> dict[str, float]:
        """Ein Messwert: Eingangsspannung plus Rauschen, bei Drift plus wachsender Versatz."""
        drift_v = 0.0
        if self._sim.has_fault("drift"):
            if count_drift:
                self._drift_samples += 1
            drift_v = self._drift_samples * DRIFT_PER_SAMPLE * self.setpoint_voltage_v
        noise_v = rng.gauss(0, 0.001 * self.setpoint_voltage_v + 0.001)
        temperature_c = 28.0 + 0.12 * self.setpoint_voltage_v + rng.gauss(0, 0.2)
        return {
            "voltage_v": round(self.setpoint_voltage_v + noise_v + drift_v, 4),
            "temperature_c": round(temperature_c, 2),
        }

    def _register_name(self, address: int) -> str:
        for name, known in self.spec.registers.items():
            if known == address:
                return name
        raise SimulationError(f"Register {address} gibt es auf {self.spec.device_id} nicht", 404)


class Simulation:
    """Alle simulierten Geräte, Zeitfaktor, Seed und aktive Fehler."""

    def __init__(self, time_scale: float = 0.1, seed: str = "42") -> None:
        self.time_scale = time_scale
        self.seed = seed
        self.faults: set[Fault] = set()
        self.devices = {spec.device_id: Device(spec, self) for spec in DEVICE_SPECS}

    @classmethod
    def from_env(cls) -> Simulation:
        return cls(float(os.environ.get("SIM_TIME_SCALE", "0.1")), os.environ.get("SIM_SEED", "42"))

    def device(self, device_id: str) -> Device:
        if device_id not in self.devices:
            known = ", ".join(self.devices)
            raise SimulationError(f"Gerät {device_id} gibt es nicht (vorhanden: {known})", 404)
        return self.devices[device_id]

    def has_fault(self, fault: Fault) -> bool:
        return fault in self.faults

    def reset(self) -> None:
        """Alles zurück auf Anfang: keine Fehler, alle Geräte aus."""
        self.faults.clear()
        for device in self.devices.values():
            device.reset()
