*** Settings ***
Documentation       Workflow-Schicht: Inbetriebnahme über die Web-Oberfläche.

Resource            src/resources/fachlich/statusseite.resource

Keyword Tags        workflow


*** Keywords ***
Gerät über Statusseite in Betrieb nehmen
    [Documentation]    Schaltet das Gerät auf der Statusseite ein und prüft, dass es messbereit wird.
    Gerät über Statusseite einschalten
    Angezeigte Betriebsbereitschaft prüfen
