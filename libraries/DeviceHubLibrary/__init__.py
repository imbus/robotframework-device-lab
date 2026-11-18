"""DeviceHubLibrary: Robot-Framework-Library für das simulierte Messmodul MM-100."""

import time
from datetime import timedelta
from enum import StrEnum
from typing import Any

from robot.api import logger
from robot.api.deco import keyword, library

from .checks import check_readings, failure_message, readings_table
from .client import DeviceHubClient, DeviceHubError
from .model import DeviceProfile, Reading
from .profile import ProfileError, load_profile

POLL_INTERVAL_S = 0.25


class DeviceState(StrEnum):
    """Zustände des Messgeräts."""

    OFF = "OFF"
    BOOTING = "BOOTING"
    SETTLING = "SETTLING"
    READY = "READY"
    MEASURING = "MEASURING"
    FAULT = "FAULT"


@library(scope="SUITE", version="0.1.0")
class DeviceHubLibrary:
    """Spricht über REST mit dem Messgerät im DeviceHub und prüft Messwerte gegen Soll-Werte.

    Grundlage ist ein *Geräteprofil* (``testdata/devices/*.json``) mit Modell, Variante,
    Registeradressen, Steuerwerten und Messpunkten. So bleiben die Tests für alle Varianten
    gleich. Profil und Verbindung gelten jeweils für eine Suite. Eine *Messgruppe* sind alle
    Messpunkte des Profils.

    = Ablauf =

    | `Load Device Profile`               | testdata/devices/variante_a.json |
    | `Connect To DeviceHub`              | http://127.0.0.1:8080            |
    | `Power On Device`                   |                                  |
    | `Wait Until Device State Is`        | READY                            |
    | ${messwerte}=                       | `Run Measurement Group`          |
    | `Readings Should Match Expectation` | ${messwerte}                     |
    | `Reset Device To Safe State`        |                                  |
    """

    def __init__(self) -> None:
        self._profile: DeviceProfile | None = None
        self._client: DeviceHubClient | None = None
        self._device_id: str | None = None

    @keyword
    def load_device_profile(self, path: str) -> DeviceProfile:
        """Lädt das Geräteprofil aus einer JSON-Datei; es gilt für alle Keywords der Suite.

        Fehlerhafte Dateien scheitern mit einer Meldung, die Feld und Erwartung nennt.

        | Load Device Profile    testdata/devices/variante_a.json
        """
        profile = load_profile(path)
        logger.info(
            f"Geräteprofil {profile.model} Variante {profile.variant} aus {profile.source}: "
            f"{len(profile.measurement_points)} Messpunkte, je {profile.repetitions} Messungen"
        )
        self._profile = profile
        return profile

    @keyword("Connect To DeviceHub")
    def connect_to_devicehub(self, url: str = "http://127.0.0.1:8080") -> None:
        """Verbindet sich mit DeviceHub und wählt das Gerät passend zu Modell und Variante."""
        profile = self._require_profile()
        client = DeviceHubClient(url)
        devices = client.request("GET", "/devices")
        for device in devices:
            if device["model"] == profile.model and device["variant"] == profile.variant:
                self._client, self._device_id = client, device["id"]
                logger.info(f"Verbunden mit {url}: Gerät {device['id']} ({device['state']})")
                return
        available = ", ".join(f"{d['model']} {d['variant']} ({d['id']})" for d in devices)
        raise DeviceHubError(
            f"DeviceHub kennt kein Gerät {profile.model} Variante {profile.variant}. "
            f"Vorhanden: {available}"
        )

    @keyword
    def get_device_metadata(self) -> dict[str, str]:
        """Liefert Gerätedaten für die Suite-Metadaten.

        Schlüssel: ``device_id``, ``model``, ``variant``, ``serial_number``, ``firmware_version``.
        """
        device = self._request("GET")
        return {
            "device_id": device["id"],
            "model": device["model"],
            "variant": device["variant"],
            "serial_number": device["serial_number"],
            "firmware_version": device["firmware_version"],
        }

    @keyword
    def power_on_device(self) -> None:
        """Schaltet das Gerät ein; es fährt hoch (``BOOTING``) und schwingt ein (``SETTLING``)."""
        state = self._request("POST", "/power", {"on": True})["state"]
        logger.info(f"Gerät {self._device_id} eingeschaltet, Zustand {state}")

    @keyword
    def power_off_device(self) -> None:
        """Schaltet das Gerät aus; im Mock wird dabei auch die Eingangsspannung auf 0 V gesetzt.

        Für Teardowns ist `Reset Device To Safe State` gedacht: Es bewirkt dasselbe, scheitert
        aber nicht, wenn noch kein Gerät verbunden ist.
        """
        state = self._request("POST", "/power", {"on": False})["state"]
        logger.info(f"Gerät {self._device_id} ausgeschaltet, Zustand {state}")

    @keyword
    def wait_until_device_state_is(
        self, state: DeviceState, timeout: timedelta | None = None
    ) -> None:
        """Wartet, bis das Gerät den Zustand ``state`` meldet, und fragt dazu regelmäßig nach.

        Ohne ``timeout`` gilt ``control.settle_timeout_s`` aus dem Geräteprofil.
        Meldet das Gerät ``FAULT``, scheitert das Keyword sofort.

        | Wait Until Device State Is    READY
        | Wait Until Device State Is    OFF    timeout=5 s
        """
        limit_s = (
            timeout.total_seconds()
            if timeout is not None
            else self._require_profile().settle_timeout_s
        )
        start = time.monotonic()
        last = None
        while True:
            current = DeviceState(self._request("GET", "/state")["state"])
            elapsed_s = time.monotonic() - start
            if current != last:
                logger.info(f"Zustand {current} nach {elapsed_s:.1f} s")
                last = current
            if current == state:
                return
            if current == DeviceState.FAULT:
                raise AssertionError(f"Gerät {self._device_id} meldet FAULT statt {state}.")
            if elapsed_s >= limit_s:
                raise AssertionError(
                    f"Gerät {self._device_id} hat den Zustand {state} "
                    f"nicht innerhalb von {limit_s:g} s "
                    f"erreicht. Letzter Zustand: {current}."
                )
            time.sleep(POLL_INTERVAL_S)

    @keyword
    def write_register(self, name: str, value: float) -> None:
        """Schreibt einen Wert in ein Register; die Adresse steht im Geräteprofil.

        | Write Register    setpoint_voltage    12.0
        """
        address = self._address(name)
        self._request("PUT", f"/registers/{address}", {"value": value})
        logger.info(f"Register {name} ({address}) ← {value:g}")

    @keyword
    def read_register(self, name: str) -> float:
        """Liest ein Register; die Adresse steht im Geräteprofil.

        | ${spannung}=    Read Register    measured_voltage
        """
        address = self._address(name)
        value = self._request("GET", f"/registers/{address}")["value"]
        logger.info(f"Register {name} ({address}) = {value:g}")
        return value

    @keyword
    def run_measurement_group(self) -> list[Reading]:
        """Misst alle Messpunkte des Geräteprofils und gibt die Messwerte zurück.

        Je Messpunkt: Eingangsspannung schreiben, Einschwingen abwarten (``READY``) und
        ``control.repetitions`` Messungen ausführen. Die Schleife über die Messpunkte
        liegt bewusst in Python, nicht im Robot-Code. Die Messwerte liefert DeviceHub als
        Messauftrag; `Read Register` liest Einzelwerte.

        | ${messwerte}=    Run Measurement Group
        """
        profile = self._require_profile()
        readings: list[Reading] = []
        for point in profile.measurement_points:
            logger.info(f"Messpunkt {point.name}: {point.input_voltage_v:g} V einstellen")
            self.write_register("setpoint_voltage", point.input_voltage_v)
            self.wait_until_device_state_is(DeviceState.READY)
            self._request("POST", "/measurements", {"repetitions": profile.repetitions})
            self.wait_until_device_state_is(DeviceState.READY)
            values = self._request("GET", "/measurements")["values"]
            logger.info(
                f"Messpunkt {point.name}: " + ", ".join(f"{v['voltage_v']:.3f} V" for v in values)
            )
            readings += [
                Reading(point.name, number, value["voltage_v"], value["temperature_c"])
                for number, value in enumerate(values, start=1)
            ]
        return readings

    @keyword
    def readings_should_match_expectation(self, readings: list[Reading]) -> None:
        """Prüft Messwerte gegen die Soll-Werte aus dem Profil und zeigt sie als Tabelle im Log.

        Scheitert mit einer Liste der abweichenden Messwerte.

        | Readings Should Match Expectation    ${messwerte}
        """
        if not readings:
            raise AssertionError("Keine Messwerte zum Prüfen übergeben.")
        checks = check_readings(readings, self._require_profile())
        logger.info(readings_table(checks), html=True)
        if not all(check.passed for check in checks):
            raise AssertionError(failure_message(checks))

    @keyword
    def reset_device_to_safe_state(self) -> None:
        """Bringt das Gerät in den sicheren Zustand: aus, Eingangsspannung 0 V. Für Teardowns.

        Ist noch kein Gerät verbunden, etwa weil die Vorbereitung früh scheiterte, gibt es
        nichts zurückzusetzen; das Keyword protokolliert das und ist erfolgreich.
        """
        if self._device_id is None:
            logger.info("Kein Gerät verbunden, nichts zurückzusetzen.")
            return
        state = self._request("POST", "/reset")["state"]
        logger.info(f"Gerät {self._device_id} zurückgesetzt: {state}, Eingangsspannung 0 V")

    def _require_profile(self) -> DeviceProfile:
        if self._profile is None:
            raise RuntimeError("Kein Geräteprofil geladen. Zuerst 'Load Device Profile' aufrufen.")
        return self._profile

    def _request(self, method: str, path: str = "", body: dict | None = None) -> Any:
        """REST-Aufruf für das verbundene Gerät, z. B. ``POST /devices/mm100-a/power``."""
        if self._client is None:
            raise RuntimeError(
                "Nicht mit DeviceHub verbunden. Zuerst 'Connect To DeviceHub' aufrufen."
            )
        return self._client.request(method, f"/devices/{self._device_id}{path}", body)

    def _address(self, name: str) -> int:
        registers = self._require_profile().registers
        if name not in registers:
            known = ", ".join(registers)
            raise ProfileError(f"Register '{name}' fehlt im Geräteprofil (bekannt: {known}).")
        return registers[name]
