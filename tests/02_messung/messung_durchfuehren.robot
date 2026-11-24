*** Comments ***
Botschaft: Der Test liest sich wie die Prüfvorschrift – Technik und Daten stehen eine Ebene tiefer.
Vorhersage: Wo im Log steht, welche Anforderung dieser Test prüft?


*** Settings ***
Documentation    Messung über alle Messpunkte des Geräteprofils.
...              Derselbe Test prüft jede Variante; welche, bestimmt das Profil in robot.toml.

Resource         src/resources/fachlich/geraet.resource
Resource         src/resources/workflow/messung.resource

# Aus QF-Test bekannt: Vorbereitung → Setup, Aufräumen → Teardown, Prozedur → Keyword
Suite Setup      Prüfstand vorbereiten
Test Setup       Gerät hochfahren
Test Teardown    Gerät in sicheren Zustand bringen

Test Tags        messung


*** Test Cases ***
Messwerte im Toleranzband
    [Documentation]    Alle Messpunkte liefern Spannungen und Temperaturen innerhalb der Grenzen.
    [Metadata]    Anforderung    [https://example.com|REQ-MM100-012]
    [Metadata]    Prüfvorschrift    PV-MM100-03 Messgenauigkeit
    ${messwerte}=    Messung durchführen
    Messergebnis bewerten    ${messwerte}
