"""Werte-Objekte: das Geräteprofil aus den Testdaten und die gemessenen Werte."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Expectation:
    """Soll-Werte eines Messpunkts."""

    voltage_v: float
    tolerance_v: float
    max_temperature_c: float


@dataclass(frozen=True)
class MeasurementPoint:
    """Ein Messpunkt: welche Spannung eingestellt wird und was dann erwartet ist."""

    name: str
    input_voltage_v: float
    expected: Expectation


@dataclass(frozen=True)
class DeviceProfile:
    """Testdaten einer Gerätevariante, gegliedert nach Testdatenarten wie die JSON-Datei."""

    source: Path
    # device
    model: str
    variant: str
    # environment
    registers: dict[str, int]
    # control
    settle_timeout_s: float
    repetitions: int
    # measurement_points
    measurement_points: tuple[MeasurementPoint, ...]

    def point(self, name: str) -> MeasurementPoint:
        for point in self.measurement_points:
            if point.name == name:
                return point
        known = ", ".join(p.name for p in self.measurement_points)
        raise ValueError(
            f"Messpunkt '{name}' steht nicht im Geräteprofil {self.source} (bekannt: {known})"
        )


@dataclass(frozen=True)
class Reading:
    """Ein gemessener Wert eines Messpunkts."""

    point: str
    repetition: int
    voltage_v: float
    temperature_c: float
