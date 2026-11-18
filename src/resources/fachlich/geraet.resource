*** Settings ***
Documentation       Fachliche Schicht: Gerät vorbereiten und in einen sicheren Zustand bringen.
...                 Die technische Schicht ist die Python-Library DeviceHubLibrary.

Library             DeviceHubLibrary

Keyword Tags        fachlich


*** Keywords ***
Prüfstand vorbereiten
    [Documentation]    Lädt das Geräteprofil, verbindet das Gerät und stellt die Simulation ein.
    Load Device Profile    ${GERAETEPROFIL}
    Connect To DeviceHub    ${DEVICEHUB_URL}
    ${gerät}=    Get Device Metadata
    Set Suite Metadata    Firmware    ${gerät}[firmware_version]
    Set Suite Metadata    Seriennummer    ${gerät}[serial_number]
    Set Suite Metadata    Variante    ${gerät}[model] ${gerät}[variant]
    Set Simulated Fault    ${SIMULATIONSFEHLER}

Gerät hochfahren
    [Documentation]    Schaltet das Gerät ein und wartet, bis es messbereit ist.
    Power On Device
    Wait Until Device State Is    READY

Gerät in sicheren Zustand bringen
    [Documentation]    Schaltet das Gerät aus und nimmt die Eingangsspannung weg; läuft immer.
    Reset Device To Safe State
