*** Settings ***
Documentation    Smoke-Test: Ist das Messgerät im DeviceHub erreichbar?
...              Prüft die Gerätedaten direkt, ohne Workflow (Ausnahme von der Schichtregel).

Resource         src/resources/fachlich/geraet.resource

Suite Setup      Prüfstand vorbereiten

Test Tags        smoke


*** Test Cases ***
Firmware lesen
    [Documentation]    Das Gerät meldet seine Firmware-Version.
    [Metadata]    Firmware    ${GERAET}[firmware_version]
    [Metadata]    Seriennummer    ${GERAET}[serial_number]
    [Metadata]    Variante    ${GERAET}[model] ${GERAET}[variant]
    Should Not Be Empty    ${GERAET}[firmware_version]
    Log    Firmware ${GERAET}[firmware_version] auf Gerät ${GERAET}[device_id]
