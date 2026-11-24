*** Comments ***
KI-Joker (Screencast): Ein lokales Vision-Modell liest die Statusseite wie ein Mensch ab.
Das Ergebnis ist typisiert (DisplayReading: Wert, Einheit) und wird gegen REST geprüft.
Starten mit: just ki; Einrichtung und Modellwahl: tests/05_ai/README.md
Ausnahme von den Schichtregeln (wie tests/01_smoke): Die Datei soll für sich allein lesbar sein.


*** Settings ***
Documentation    KI-Joker: Die Statusseite zeigt denselben Messwert an, den das Gerät über REST liefert.

Library          AIAgent.Agent    ${KI_MODELL}
Library          AIAgent.Content
Library          Browser
Library          DeviceHubLibrary
Library          display_reading
Resource         src/resources/fachlich/geraet.resource

Suite Setup      Prüfstand vorbereiten
Test Teardown    Gerät in sicheren Zustand bringen

Test Tags        ki


*** Variables ***
# Lokales Modell über Ollama; anderes Modell: just ki --variable KI_MODELL:ollama:<name>
${KI_MODELL}    ollama:qwen3-vl:8b


*** Test Cases ***
Irgendeine Frage
    [Setup]    ${None}
    ${result}    Chat    Wie wird das Wetter morgen in Köln?
    Log    ${result}
    [Teardown]    ${None}

Statusseite zeigt den REST-Messwert an
    [Documentation]    Das Modell liest den Messwert vom Bildschirmfoto; er passt zum REST-Messwert.
    Gerät mit 12 V betreiben
    Statusseite öffnen
    ${messwert_abgelesen}=    Messwert mit KI ablesen
    Abgelesenen Messwert prüfen    ${messwert_abgelesen}
    Log    ${messwert_abgelesen.value} ${messwert_abgelesen.unit}

*** Keywords ***
Gerät mit 12 V betreiben
    [Documentation]    Fährt das Gerät hoch und legt 12 V Eingangsspannung an.
    Gerät hochfahren
    Write Register    setpoint_voltage    12
    Wait Until Device State Is    READY

Statusseite öffnen
    [Documentation]    Öffnet die Statusseite des Geräts und wartet, bis sie READY anzeigt.
    New Browser    chromium    headless=False
    New Page    ${DEVICEHUB_URL}/ui/devices/${GERAET}[device_id]
    Wait For Condition    Text    data-testid=device-state    ==    READY

Messwert mit KI ablesen
    [Documentation]    Fotografiert die Statusseite und lässt das Modell Wert und Einheit ablesen.
    ${foto}=    Take Screenshot    filename=statusseite
    ${bild}=    Load Binary Content    ${foto}
    ${anzeige}=    Chat    Welcher Messwert steht auf dieser Statusseite? Wert und Einheit.    
    ...    ${bild}
    ...    output_type=${{display_reading.DisplayReading}}
    RETURN    ${anzeige}

Abgelesenen Messwert prüfen
    [Documentation]    Vergleicht den abgelesenen Wert mit dem Messwert, den das Gerät über REST liefert.
    [Arguments]    ${anzeige}
    ${messwert}=    Read Register    measured_voltage
    Display Reading Should Match    ${anzeige}    ${messwert}
