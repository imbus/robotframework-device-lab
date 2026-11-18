*** Settings ***
Documentation    Smoke-Test: Ist das Messgerät im DeviceHub erreichbar?
...              Ruft die Library bewusst direkt auf (Ausnahme von der Schichtregel).

Library          DeviceHubLibrary

Suite Setup      Gerät verbinden

Test Tags        smoke


*** Test Cases ***
Firmware lesen
    [Documentation]    Das Gerät meldet seine Firmware-Version.
    ${metadaten}=    Get Device Metadata
    Should Not Be Empty    ${metadaten}[firmware_version]
    Log    Firmware ${metadaten}[firmware_version] auf Gerät ${metadaten}[device_id]


*** Keywords ***
Gerät verbinden
    [Documentation]    Lädt das Geräteprofil, verbindet sich mit dem DeviceHub
    ...    und setzt die Suite-Metadaten.
    Load Device Profile    ${GERAETEPROFIL}
    Connect To DeviceHub    ${DEVICEHUB_URL}
    ${metadaten}=    Get Device Metadata
    Set Suite Metadata    Firmware    ${metadaten}[firmware_version]
    Set Suite Metadata    Seriennummer    ${metadaten}[serial_number]
    Set Suite Metadata    Variante    ${metadaten}[model] ${metadaten}[variant]
