# Nach dem Workshop: Ausbau zum Leuchtturm-Projekt

Bewusst zurückgestellt, damit der Workshop rechtzeitig fertig wird. Sessions dürfen hier
Ideen ergänzen, statt sie sofort zu bauen.

## Qualität und Werkzeuge
- Jenkins vollständig als Code (Configuration as Code, Job DSL)
- Offline-Betrieb: `just offline-prepare` (Images, Pakete, Browser vorab laden);
  in S3 gestrichen, weil vor Ort WLAN da ist
- pre-commit mit Robocop, ruff, pytest
- Devcontainer für einen Start mit einem Befehl
- Eigene Robocop-Regeln (kein `Sleep`, Pflicht-Dokumentation, Schichtregeln)
- Umfassende Unit-Tests für Mock und Library

## Dokumentation
- ADRs: drei Schichten, Testdaten als Werte-Objekte, Robot vs. Python, Sprachentscheidung
- CONTRIBUTING mit Keyword-Regeln und Review-Ablauf
- Glossar mit vollständiger QF-Test-Übersetzung

## Fachliche Erweiterungen
- JSON-Schema für Testdaten
- Listener, der Messwerte exportiert und grafisch aufbereitet
- Legacy-Web-UI ohne test-ids
- Display-Ansicht im Mock, zweite KI-Demo mit rf-mcp
- Parallele Messgruppen, weitere Fehlerarten (Timeout, falscher Wert)
- Anbindung an ein Testmanagement-Werkzeug

## Beispiele (bewusst weggelassen, Botschaft tragen vorhandene Dateien)
- Ordner `beispiele/` mit eigenem Kontrastpaar „Einzelschritte vs. Prüfvorschrift“ – trägt heute
  `tests/antipatterns/` ↔ `tests/02_messung/`
- Beispiel „Robot beschreibt, Python rechnet“ mit typisiertem Python-Keyword
- Beispieldatei „bereit für die Pipeline“ (Tags, Metadata, drei Aufrufe) – tragen heute Profile und Jenkins
- Übungen mit Lückentexten für Teilnehmende

## Weiterverwendung
- Repo als Vorlage für weitere Projekte verallgemeinern
- Diagramme und Folien als wiederverwendbares Schulungsmodul
