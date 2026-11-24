"""KI-Joker: typisiertes Ergebnis des Vision-Modells und Vergleich mit dem REST-Messwert.

Robot beschreibt, Python rechnet: Einheit und Toleranz prüft dieses Keyword, nicht der Robot-Code.
"""

from dataclasses import dataclass

from robot.api.deco import keyword

ROBOT_AUTO_KEYWORDS = False

TOLERANCE = 0.01  # 1 % des REST-Messwerts, wie in den Geräteprofilen


@dataclass
class DisplayReading:
    """Messwert, wie ihn das Modell auf der Statusseite abliest."""

    value: float
    unit: str


@keyword
def display_reading_should_match(reading: DisplayReading, measured_v: float) -> None:
    """Prüft den abgelesenen Wert gegen den REST-Messwert: Einheit V, Abweichung höchstens 1 %.

    | Display Reading Should Match    ${anzeige}    ${messwert}
    """
    if reading.unit.strip() != "V":
        raise AssertionError(f"Einheit: erwartet V, abgelesen {reading.unit!r}.")
    allowed_v = TOLERANCE * abs(measured_v)
    deviation_v = abs(reading.value - measured_v)
    if deviation_v > allowed_v:
        raise AssertionError(
            f"Anzeige {reading.value:g} V, REST {measured_v:.3f} V: "
            f"Abweichung {deviation_v:.3f} V, erlaubt höchstens {allowed_v:.3f} V."
        )
