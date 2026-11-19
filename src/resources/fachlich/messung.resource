*** Settings ***
Documentation    Fachliche Schicht: Messwerte aufnehmen, protokollieren und bewerten.
...              Die technische Schicht ist die Python-Library DeviceHubLibrary.

Library          DeviceHubLibrary

Keyword Tags     fachlich


*** Keywords ***
Messwerte erhalten
    [Documentation]    Stellt nacheinander alle Messpunkte ein und liefert die Messwerte.
    ${messwerte}=    Run Measurement Group
    RETURN    ${messwerte}

Messprotokoll erstellen
    [Documentation]    Zeigt Soll, Ist, Toleranz und Ergebnis aller Messwerte als Tabelle im Log.
    [Arguments]    ${messwerte}
    Log Readings Table    ${messwerte}

Spannungen prüfen
    [Documentation]    Prüft, ob alle Spannungen im Toleranzband der Soll-Werte liegen.
    [Arguments]    ${messwerte}
    Voltages Should Be Within Tolerance    ${messwerte}

Temperaturen prüfen
    [Documentation]    Prüft, ob keine Temperatur den Grenzwert überschreitet.
    [Arguments]    ${messwerte}
    Temperatures Should Stay Below Limit    ${messwerte}
