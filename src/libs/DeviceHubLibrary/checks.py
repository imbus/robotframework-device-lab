"""Prüft Messwerte gegen die Soll-Werte und stellt das Ergebnis als HTML-Tabelle dar."""

from collections.abc import Callable
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


def voltage_failures(checks: list[Check]) -> str | None:
    """Fehlermeldung für Spannungen außerhalb der Toleranz, None wenn alle passen."""
    failed = [check for check in checks if not check.voltage_ok]
    return _message(
        checks,
        failed,
        "Spannungen außerhalb der Toleranz",
        lambda r, e: (
            f"erwartet {e.voltage_v:.3f} V ± {e.tolerance_v:.3f} V, gemessen {r.voltage_v:.3f} V"
        ),
    )


def temperature_failures(checks: list[Check]) -> str | None:
    """Fehlermeldung für Temperaturen über dem Grenzwert, None wenn alle passen."""
    failed = [check for check in checks if not check.temperature_ok]
    return _message(
        checks,
        failed,
        "Temperaturen über dem Grenzwert",
        lambda r, e: f"{r.temperature_c:.1f} °C, erlaubt höchstens {e.max_temperature_c:g} °C",
    )


def _message(
    checks: list[Check],
    failed: list[Check],
    title: str,
    describe: Callable[[Reading, Expectation], str],
) -> str | None:
    if not failed:
        return None
    lines = [f"{len(failed)} von {len(checks)} Messwerten: {title}"]
    lines += [
        f"{c.reading.point} Messung {c.reading.repetition}: {describe(c.reading, c.expected)}"
        for c in failed[:_MAX_LISTED_FAILURES]
    ]
    if len(failed) > _MAX_LISTED_FAILURES:
        lines.append(f"… und {len(failed) - _MAX_LISTED_FAILURES} weitere (siehe Tabelle im Log)")
    return "\n".join(lines)


_HEADERS = ("Messpunkt", "Nr.", "Soll", "Ist", "Abweichung", "Toleranz", "Temperatur", "Ergebnis")
# Feste dunkle Schrift: Im dunklen Log-Design wäre sie sonst hellgrau auf hellem Zellhintergrund.
_CELL = (
    "border:1px solid #c8ccd2;padding:3px 10px;text-align:right;white-space:nowrap;color:#1f1f1f"
)


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
