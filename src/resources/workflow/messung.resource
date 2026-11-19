*** Settings ***
Documentation    Workflow-Schicht: der Messablauf in der Sprache des Fachbereichs.

Resource         src/resources/fachlich/messung.resource

Keyword Tags     workflow


*** Keywords ***
Messung durchführen
    [Documentation]    Misst alle Messpunkte des Geräteprofils und protokolliert die Messwerte.
    ${messwerte}=    Messwerte erhalten
    Messprotokoll erstellen    ${messwerte}
    RETURN    ${messwerte}

Messergebnis bewerten
    [Documentation]    Prüft Spannungen und Temperaturen gegen die Soll-Werte des Geräteprofils.
    [Arguments]    ${messwerte}
    Spannungen prüfen    ${messwerte}
    Temperaturen prüfen    ${messwerte}
