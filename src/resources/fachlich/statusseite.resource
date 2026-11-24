*** Settings ***
Documentation    Fachliche Schicht: das Gerät über seine Statusseite bedienen.
...              Die technische Schicht ist die Browser Library; Selektoren nur in dieser Datei.

Library          Browser
Library          DeviceHubLibrary

Keyword Tags     fachlich


*** Variables ***
${HEADLESS}    ${False}


*** Keywords ***
Gerät über Statusseite einschalten
    [Documentation]    Öffnet die Statusseite des verbundenen Geräts und klickt dort auf „Ein“.
    ${gerät}=    Get Device Metadata
    New Browser    chromium    headless=${HEADLESS}
    New Page    ${DEVICEHUB_URL}/ui/devices/${gerät}[device_id]
    Click    data-testid=power-on

Angezeigte Betriebsbereitschaft prüfen
    [Documentation]    Wartet, bis die Statusseite das Gerät als messbereit (READY) anzeigt.
    Wait For Condition    Text    data-testid=device-state    ==    READY    timeout=15 s

Status des Geräts entspricht
    [Arguments]    ${status: Literal['OFF', 'BOOTING', 'SETTLING', 'READY', 'MEASURING', 'FAULT']}
    ${text}    Get Text    data-testid=device-state
    Should Be Equal    ${text}    ${status}

