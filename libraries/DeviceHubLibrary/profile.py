"""Lädt ein Geräteprofil (testdata/devices/*.json) in Werte-Objekte.

Fehlerhafte Dateien scheitern mit einer Meldung, die Feld und Erwartung nennt, z. B.:
Geräteprofil kaputt.json fehlerhaft: Feld 'control.repetitions' ist "drei"
– erwartet: ganze Zahl ≥ 1
"""

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

from .model import DeviceProfile, Expectation, MeasurementPoint

REQUIRED_REGISTERS = ("setpoint_voltage", "measured_voltage", "temperature", "status")


class ProfileError(Exception):
    """Die Testdaten-Datei fehlt, ist kein JSON oder passt nicht zum Format."""

    ROBOT_SUPPRESS_NAME = True


class _FieldError(Exception):
    def __init__(self, field: str, problem: str, expected: str) -> None:
        super().__init__(f"Feld '{field}' {problem} – erwartet: {expected}")


def load_profile(path: str | Path) -> DeviceProfile:
    path = Path(path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ProfileError(f"Geräteprofil nicht gefunden: {path}") from None
    except json.JSONDecodeError as error:
        raise ProfileError(
            f"Geräteprofil {path} ist kein gültiges JSON: {error.msg} "
            f"(Zeile {error.lineno}, Spalte {error.colno})"
        ) from None
    try:
        return _parse(_Section(data, ""), path)
    except _FieldError as error:
        raise ProfileError(f"Geräteprofil {path} fehlerhaft: {error}") from None


def _parse(root: _Section, source: Path) -> DeviceProfile:
    device = root.section("device")
    registers = root.section("environment").section("registers")
    control = root.section("control")
    return DeviceProfile(
        source=source,
        model=device.text("model"),
        variant=device.text("variant"),
        registers={name: registers.integer(name) for name in REQUIRED_REGISTERS},
        settle_timeout_s=control.number("settle_timeout_s"),
        repetitions=control.integer("repetitions"),
        measurement_points=tuple(
            _measurement_point(point) for point in root.sections("measurement_points")
        ),
    )


def _measurement_point(point: _Section) -> MeasurementPoint:
    expected = point.section("expected")
    return MeasurementPoint(
        name=point.text("name"),
        input_voltage_v=point.section("input").number("voltage_v"),
        expected=Expectation(
            voltage_v=expected.number("voltage_v"),
            tolerance_v=expected.number("tolerance_v"),
            max_temperature_c=expected.number("max_temperature_c"),
        ),
    )


class _Section:
    """Ein JSON-Objekt mit seinem Pfad, damit jede Fehlermeldung das genaue Feld nennt."""

    def __init__(self, data: object, path: str) -> None:
        if not isinstance(data, dict):
            raise _FieldError(path or "(Datei)", f"ist {_show(data)}", "Objekt { … }")
        self._data = data
        self._path = path

    def section(self, key: str) -> _Section:
        return _Section(self._get(key, "Objekt { … }"), self._field(key))

    def sections(self, key: str) -> list[_Section]:
        entries = self._get(
            key, "Liste mit mindestens einem Eintrag", lambda v: isinstance(v, list) and len(v) > 0
        )
        return [
            _Section(entry, f"{self._field(key)}[{index}]") for index, entry in enumerate(entries)
        ]

    def text(self, key: str) -> str:
        return self._get(key, "nicht leerer Text", lambda v: isinstance(v, str) and v.strip() != "")

    def number(self, key: str) -> float:
        return float(self._get(key, "Zahl ≥ 0", lambda v: type(v) in (int, float) and v >= 0))

    def integer(self, key: str) -> int:
        return self._get(key, "ganze Zahl ≥ 1", lambda v: type(v) is int and v >= 1)

    def _get(self, key: str, expected: str, valid: Callable[[Any], bool] | None = None) -> Any:
        if key not in self._data:
            raise _FieldError(self._field(key), "fehlt", expected)
        value = self._data[key]
        if valid is not None and not valid(value):
            raise _FieldError(self._field(key), f"ist {_show(value)}", expected)
        return value

    def _field(self, key: str) -> str:
        return f"{self._path}.{key}" if self._path else key


def _show(value: object) -> str:
    return json.dumps(value, ensure_ascii=False)
