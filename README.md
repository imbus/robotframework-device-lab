# robotframework-device-lab

Robot Framework testet über REST ein simuliertes Messmodul MM-100 (Varianten A und B), das im
Mock-Werkzeug DeviceHub läuft. Alles ist frei erfunden und läuft lokal.

## Voraussetzungen

- [uv](https://docs.astral.sh/uv/) (installiert Python und alle Pakete)
- [just](https://github.com/casey/just) (Befehlsläufer)
- Docker Desktop oder Rancher Desktop, nur für Jenkins

## Start in drei Befehlen

```bash
just setup    # einmalig: Pakete und Browser installieren
just sim      # Terminal 1: Mock-Gerät DeviceHub starten
just test     # Terminal 2: alle Tests ausführen
```

Die Ergebnisse stehen danach in `results/log.html` und `results/report.html`.

## Die wichtigsten Befehle

`just` ohne Argument zeigt alle Befehle.

| Befehl | Was passiert |
| --- | --- |
| `just sim` | Mock-Gerät starten (API-Doku: `http://127.0.0.1:8080/docs`) |
| `just test` | alle Tests (Standard: Variante A) |
| `just test-a` / `just test-b` | alle Tests gegen Variante A bzw. B |
| `just quiz <n>` | Fehler-Quiz 1, 2 oder 3: Die Messung scheitert. Warum? |
| `just antipattern` | absichtlich schlechtes Beispiel ausführen |
| `just reset` | Demo zurücksetzen (Mock-Fehler aus, `results/` leer, neue Geräteprofile gelöscht) |
| `just lint` | Robocop prüft alle Robot-Dateien (Befunde nur im Anti-Pattern, gewollt) |
| `just format` | Robot-Dateien mit Robocop formatieren |
| `just docs` | Keyword-Doku nach `docs/keywords/` erzeugen |
| `just jenkins` / `just jenkins-stop` | lokales Jenkins starten bzw. stoppen |

## Ordner

| Ordner | Inhalt |
| --- | --- |
| `tests/` | die Testfälle: Smoke, Messung, Web-UI und das Anti-Pattern |
| `src/resources/workflow/` | Workflow-Keywords: ganze Abläufe, z. B. `Messung durchführen` |
| `src/resources/fachlich/` | fachliche Keywords: einzelne Schritte, z. B. `Spannungen prüfen` |
| `src/libs/DeviceHubLibrary/` | Python-Library: spricht REST mit dem Gerät, rechnet und prüft |
| `src/libs/tests/` | Unit-Tests der Library, starten mit `uv run pytest` |
| `data/` | Testdaten: ein JSON-Geräteprofil je Variante, dazu Daten für das Quiz |
| `devicehub/` | das Mock-Gerät (FastAPI) mit REST-API und Statusseite |
| `jenkins/` | Jenkins im Container und seine Einrichtung (Pipeline: `Jenkinsfile`) |
| `docs/` | Diagramme und die erzeugte Keyword-Doku |

## Die vier Regeln

Aufrufkette: **Test → Workflow → Fachlich → Python-Library**

1. Tests rufen nur Workflow-Keywords auf (Ausnahme: `tests/01_smoke`).
2. Keine technischen Daten im Test: keine Registeradressen, URLs oder Selektoren.
3. Keine Logik im Robot-Code: Robot beschreibt, Python rechnet.
4. Kein `Sleep`: Gewartet wird auf Zustände.

## Mehr

- Keyword-Doku: [`docs/keywords/`](docs/keywords/), erzeugen mit `just docs`
- Jenkins einrichten: [`jenkins/EINRICHTUNG.md`](jenkins/EINRICHTUNG.md)
