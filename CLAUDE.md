# CLAUDE.md – robotframework-device-lab

Kontext für jede Claude-Code-Session in diesem Repo. Erst lesen, dann arbeiten.

## Worum es geht

Dieses Repo ist das Vorführprojekt für einen eintägigen Robot-Framework-Workshop
(25.11.2026, ca. 20 Teilnehmende, nur Zuhören mit Live-Demos).

**Leitlinie: Workshop zuerst.** Gebaut wird nur, was auf einer Folie oder in einer Demo
vorkommt. Alles Weitere steht in `plan/LEUCHTTURM.md` und kommt nach dem Workshop.
Einfach und gut lesbar schlägt vollständig.

Fachlicher Hintergrund (generisch, ohne Kundendaten): Firmware von Messgeräten wird über ein
REST-Werkzeug getestet. Robot Framework ist die **Steuerzentrale**: Es liest Testdaten aus
JSON-Dateien, spricht über REST mit dem Gerät, prüft Messwerte gegen Soll-Werte und erzeugt
lesbare Berichte. Gerätevarianten unterscheiden sich in Registeradressen und Soll-Werten,
die Tests bleiben generisch.

## Harte Regeln

- **Keine Kundendaten, keine Kundennamen, keine Kopien interner Kundenwerkzeuge.** Alles ist
  generisch und frei erfunden. Das Mock-Werkzeug heißt `DeviceHub`.
- **Alles läuft lokal** (macOS, Apple Silicon; Docker Desktop oder Rancher Desktop nur für Jenkins).
- **Ohne Internet lauffähig** nach `just setup` (Mock und Tests); Jenkins braucht Internet nur
  beim ersten Bau des Images.
- **Vorführtauglich:** kurze, gut lesbare Ausgaben, ein Befehl pro Aktion (`just …`, Liste: `just`).

## Namen

| Was | Name |
|---|---|
| Repo | `robotframework-device-lab` |
| Mock-Werkzeug (REST) | `DeviceHub` (Python-Paket `devicehub`) |
| Gerät | Messmodul `MM-100`, Varianten `A` und `B` (der Mock kennt zusätzlich `C` für die Demo „neues Gerät“) |
| Python-Library | `DeviceHubLibrary` |

## Tech-Stack (Versionen in `uv.lock`)

- Python 3.14, **uv**
- Robot Framework 7.x, **RobotCode** (VS Code und CLI) mit `robot.toml` und Profilen
- Browser Library mit **Browser Batteries** (bringt Node.js mit) für den einen Web-UI-Test
- FastAPI + Uvicorn für den Mock
- **Robocop** mit Standardregeln (Konfiguration in `pyproject.toml`)
- `just` als Befehlsläufer, Jenkins lokal in Docker (`just jenkins`)

## Architektur (gTAA-Bezug)

```
Testdefinition   tests/  +  src/resources/{workflow,fachlich}/  +  data/
Testausführung   Robot Framework über RobotCode, robot.toml-Profile, lokal oder Jenkins
Testadaptierung  src/libs/DeviceHubLibrary (Python)  +  Browser Library
SUT              devicehub/ (Mock-Gerät mit REST-API und Web-UI)
```

## Die Keyword-Schichten (verbindlich)

| Schicht | Ordner | Darf aufrufen | Beispiel |
|---|---|---|---|
| Workflow | `src/resources/workflow/` | nur fachliche Keywords | `Messung durchführen`, `Messergebnis bewerten` |
| Fachlich | `src/resources/fachlich/` | Library-Keywords | `Prüfstand vorbereiten`, `Spannungen prüfen` |
| Technisch | `src/libs/DeviceHubLibrary/`, Browser | – | Python, englisch: `Run Measurement Group` |

Es gibt **keine technische Resource-Schicht**: Die Python-Library (bzw. Browser) ist die technische
Schicht; dünne 1:1-Umbenennungen in Robot wären eine Schicht zu viel.

Regeln:

1. Tests rufen **nur Workflow-Keywords** auf (Ausnahmen: `tests/01_smoke` und der KI-Joker
   `tests/05_ai` mit lokalen Keywords; Setup und Teardown rufen fachliche Keywords direkt auf).
2. **Keine technischen Daten im Test** (keine Registeradressen, URLs, Selektoren).
3. **Keine Logik im Robot-Code:** Bedingungen, Schleifen über Daten (auch über Messpunkte),
   Umrechnungen und Toleranzen gehören in Python. Robot beschreibt, Python rechnet.
4. Kein `Sleep`; gewartet wird auf Zustände.

Bewusst schlecht: `tests/04_antipatterns/` bricht alle Regeln (Tag `antipattern`, läuft nur mit
`just antipattern`, Robocop-Befunde nur dort).

## Sprache und Namen

- Robot-Dateien: **Deutsch**. Python-Code und Library-Keywords: **Englisch**.
- Keyword-Namen: ein bis sechs Wörter, Form **Objekt + Verb im Infinitiv**
  (`Gerät hochfahren`, `Messwerte prüfen`). Einheitlich `prüfen`, `einstellen`, `abwarten`.
- Jedes Keyword hat `[Documentation]` mit einem Satz.
- Variablen mit `VAR` (mit `=`), nicht mit `Set … Variable`.

## Testdaten (`data/devices/*.json`, Quiz-Daten in `data/quiz/`)

Gegliedert nach Testdatenarten:

```json
{
  "device":      { "model": "MM-100", "variant": "A" },
  "environment": { "registers": { "setpoint_voltage": 40001, "measured_voltage": 30001,
                                  "temperature": 30003, "status": 30010 } },
  "control":     { "settle_timeout_s": 15, "repetitions": 3 },
  "measurement_points": [
    { "name": "MP1", "input": { "voltage_v": 5.0 },
      "expected": { "voltage_v": 5.0, "tolerance_v": 0.05, "max_temperature_c": 60 } }
  ]
}
```

Die Library lädt die Datei in Dataclasses (Werte-Objekte); fehlerhafte Dateien scheitern mit
verständlicher Meldung (Feld und Erwartung).

## Berichte

- Gerätedaten (Firmware, Seriennummer, Variante) als `[Metadata]` am Test; `Prüfstand vorbereiten`
  stellt sie als `${GERAET}` bereit.
- Messwerte erscheinen im Log als **HTML-Tabelle** (Soll, Ist, Toleranz, Ergebnis).
- Fehlermeldungen sagen, was erwartet und was gefunden wurde.
- Fehler im Setup meldet Robot als „Setup failed: …“ mit der Meldung der Library (kein eigenes TRY).
- Teardown bringt das Gerät immer in einen sicheren Zustand.

## Arbeitsweise in Sessions

- Erst den Plan zeigen, dann umsetzen. Im Zweifel die einfachere Lösung.
- **Commits macht der Nutzer selbst.** Claude schlägt Aufteilung und deutsche Commit-Nachrichten vor.
- Prüfen mit `just …` und `uv run robotcode results …` statt langer Shell-Skripte.
- Am Ende Akzeptanzkriterien prüfen und `plan/HANDOFF.md` ergänzen.
- Ideen, die über den Auftrag hinausgehen, nicht bauen, sondern in `plan/LEUCHTTURM.md` notieren.
- Außerhalb des Repos nur `../workshop-material/` (Folien, Drehbuch; nicht öffentlich).
  Keine Geheimnisse einchecken.
