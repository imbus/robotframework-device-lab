*** Settings ***
Documentation    Fachliche Schicht: Gerät vorbereiten und in einen sicheren Zustand bringen.
...              Die technische Schicht ist die Python-Library DeviceHubLibrary.

Library          DeviceHubLibrary

Keyword Tags     fachlich


*** Variables ***
# Gerätedaten für [Metadata] in den Tests; gefüllt von „Gerätedaten bereitstellen“
&{GERAET}    &{EMPTY}


*** Keywords ***
Prüfstand vorbereiten
    [Documentation]    Lädt das Geräteprofil, verbindet das Gerät und stellt die Simulation ein.
    Load Device Profile    ${GERAETEPROFIL}
    Connect To DeviceHub    ${DEVICEHUB_URL}
    Configure Device Data
    Set Simulated Fault    ${SIMULATIONSFEHLER}

Configure Device Data
    [Documentation]    Liest Firmware, Seriennummer und Variante und stellt sie als ${GERAET} bereit.
    ${daten}=    Get Device Metadata
    VAR    &{GERAET}=    &{daten}    scope=SUITE    # robocop: off=no-suite-variable

Gerät hochfahren
    [Documentation]    Schaltet das Gerät ein und wartet, bis es messbereit ist.
    Power On Device
    Wait Until Device State Is    READY

Gerät in sicheren Zustand bringen
    [Documentation]    Schaltet das Gerät aus und nimmt die Eingangsspannung weg; läuft immer.
    Reset Device To Safe State
