*** Comments ***
Botschaft: Absichtlich schlecht – läuft grün, aber Logik, Sleep, Registeradressen und Kopien stehen
im Test; die gute Lösung ist tests/02_messung/messung_durchfuehren.robot (Block 7, Folie 18).
Vorhersage: Der Lauf ist grün – woran sieht man im Log trotzdem, dass dieser Test schlecht ist?


*** Settings ***
Library    DeviceHubLibrary
Test Tags    antipattern


*** Test Cases ***
Messung Variante A
    Load Device Profile    data/devices/variante_a.json
    Connect To DeviceHub    http://127.0.0.1:8080
    Power On Device
    Sleep    6s
    FOR    ${soll}    IN    5.0    12.0    24.0
        Write Register    40001    ${soll}
        Sleep    2s
        ${ist}=    Read Register    30001
        IF    abs(${ist} - ${soll}) > ${soll} * 0.01
            Fail    Messwert falsch
        END
    END
    Power Off Device

Messung Variante B
    Load Device Profile    data/devices/variante_b.json
    Connect To DeviceHub    http://127.0.0.1:8080
    Power On Device
    Sleep    6s
    FOR    ${soll}    IN    10.0    48.0    110.0
        Write Register    41001    ${soll}
        Sleep    2s
        ${ist}=    Read Register    31001
        IF    abs(${ist} - ${soll}) > ${soll} * 0.01
            Fail    Messwert falsch
        END
    END
    Power Off Device
