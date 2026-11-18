*** Settings ***
Documentation       Web-UI: Das Gerät lässt sich über seine Statusseite in Betrieb nehmen.
...                 Einmalig vorher: uv run rfbrowser init

Resource            src/resources/fachlich/geraet.resource
Resource            src/resources/workflow/statusseite.resource

Suite Setup         Prüfstand vorbereiten
Test Teardown       Gerät in sicheren Zustand bringen

Test Tags           ui


*** Test Cases ***
Statusseite schaltet Gerät ein
    [Documentation]    Nach „Ein“ auf der Statusseite zeigt das Gerät an, dass es messbereit ist.
    Gerät über Statusseite in Betrieb nehmen
