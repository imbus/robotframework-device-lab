"""Prüft Messwerte gegen die Soll-Werte und stellt das Ergebnis als HTML-Tabelle dar."""

from dataclasses import dataclass
from html import escape

from .model import DeviceProfile, Expectation, Reading

_MAX_LISTED_FAILURES = 5


@dataclass(frozen=True)
class Check:
    """Ein Messwert mit seinen Soll-Werten und dem Prüfergebnis."""

    reading: Reading
    expected: Expectation

    @property
    def deviation_v(self) -> float:
        # Betrag der Abweichung, gerundet: Reste wie 1.1 - 1.0 = 0.10000000000000009
        # sollen nicht über die Toleranzgrenze kippen.
        return round(abs(self.reading.voltage_v - self.expected.voltage_v), 6)

    @property
    def voltage_ok(self) -> bool:
        return self.deviation_v <= self.expected.tolerance_v

    @property
    def temperature_ok(self) -> bool:
        return self.reading.temperature_c <= self.expected.max_temperature_c

    @property
    def passed(self) -> bool:
        return self.voltage_ok and self.temperature_ok


def check_readings(readings: list[Reading], profile: DeviceProfile) -> list[Check]:
    return [Check(reading, profile.point(reading.point).expected) for reading in readings]


def failure_message(checks: list[Check]) -> str:
    failed = [check for check in checks if not check.passed]
    lines = [f"{len(failed)} von {len(checks)} Messwerten weichen von den Soll-Werten ab:"]
    lines += [_describe(check) for check in failed[:_MAX_LISTED_FAILURES]]
    if len(failed) > _MAX_LISTED_FAILURES:
        lines.append(f"… und {len(failed) - _MAX_LISTED_FAILURES} weitere (siehe Tabelle im Log)")
    return "\n".join(lines)


def _describe(check: Check) -> str:
    reading, expected = check.reading, check.expected
    problems = []
    if not check.voltage_ok:
        problems.append(
            f"erwartet {expected.voltage_v:.3f} V ± {expected.tolerance_v:.3f} V, "
            f"gemessen {reading.voltage_v:.3f} V"
        )
    if not check.temperature_ok:
        problems.append(
            f"Temperatur {reading.temperature_c:.1f} °C, "
            f"erlaubt höchstens {expected.max_temperature_c:g} °C"
        )
    return f"{reading.point} Messung {reading.repetition}: " + "; ".join(problems)


_HEADERS = ("Messpunkt", "Nr.", "Soll", "Ist", "Abweichung", "Toleranz", "Temperatur", "Ergebnis")
_CELL = "border:1px solid #c8ccd2;padding:3px 10px;text-align:right;white-space:nowrap"


def readings_table(checks: list[Check]) -> str:
    """HTML-Tabelle für das Robot-Log: eine Zeile je Messwert, Abweichungen rot."""
    passed = sum(check.passed for check in checks)
    head = "".join(f'<th style="{_CELL};background:#eef0f3">{title}</th>' for title in _HEADERS)
    rows = "".join(_row(check) for check in checks)
    return (
        '<table style="border-collapse:collapse">'
        '<caption style="text-align:left;font-weight:bold">'
        f"{passed} von {len(checks)} Messwerten in Ordnung</caption>"
        f"<tr>{head}</tr>{rows}</table>"
    )


def _row(check: Check) -> str:
    reading, expected = check.reading, check.expected
    background = "#eaf5ec" if check.passed else "#fdeceb"
    return (
        f'<tr style="background:{background}">'
        + _cell(escape(reading.point))
        + _cell(reading.repetition)
        + _cell(f"{expected.voltage_v:.3f} V")
        + _cell(f"{reading.voltage_v:.3f} V", red=not check.voltage_ok)
        + _cell(f"{check.deviation_v:.3f} V", red=not check.voltage_ok)
        + _cell(f"± {expected.tolerance_v:.3f} V")
        + _cell(
            f"{reading.temperature_c:.1f} °C (max. {expected.max_temperature_c:g})",
            red=not check.temperature_ok,
        )
        + _cell("OK" if check.passed else "nicht OK", red=not check.passed)
        + "</tr>"
    )


def _cell(text: object, red: bool = False) -> str:
    style = _CELL + (";font-weight:bold;color:#b3261e" if red else "")
    return f'<td style="{style}">{text}</td>'
