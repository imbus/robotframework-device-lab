# CLAUDE.md – rf-device-lab

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
- **Alles läuft lokal** (macOS, Apple Silicon, Rancher Desktop als Docker-Laufzeit).
- **Offline-fähig** nach einmaligem Setup.
- **Vorführtauglich:** kurze, gut lesbare Ausgaben, ein Befehl pro Aktion (`just …`).

## Namen

| Was | Name |
|---|---|
| Repo | `rf-device-lab` |
| Mock-Werkzeug (REST) | `DeviceHub` (Python-Paket `devicehub`) |
| Gerät | Messmodul `MM-100`, Varianten `A` und `B` |
| Python-Library | `DeviceHubLibrary` |

## Tech-Stack (Versionen beim ersten Setup festschreiben, `uv.lock` einchecken)

- Python 3.12, **uv**
- Robot Framework 7.x, **RobotCode** (VS Code) mit `robot.toml`
- Browser Library für den einen Web-UI-Test
- FastAPI + Uvicorn für den Mock
- **Robocop** mit Standardregeln
- `just` als Befehlsläufer

## Architektur (gTAA-Bezug)

```
Testdefinition   tests/  +  resources/{workflow,fachlich,technisch}/  +  testdata/
Testausführung   Robot Framework, robot.toml-Profile, lokal oder Jenkins
Testadaptierung  libraries/DeviceHubLibrary (Python)  +  Browser Library
SUT              devicehub/ (Mock-Gerät mit REST-API und Web-UI)
```

## Die drei Keyword-Schichten (verbindlich)

| Schicht | Ordner | Darf aufrufen | Beispiel |
|---|---|---|---|
| Workflow | `resources/workflow/` | nur fachliche Keywords | `Messung durchführen` |
| Fachlich | `resources/fachlich/` | technische Keywords | `Messpunkt einstellen`, `Messwerte prüfen` |
| Technisch | `resources/technisch/` | Library-Keywords | `Register schreiben`, `Gerätezustand abwarten` |
| (Code) | `libraries/` | – | Python, englische Keyword-Namen |

Regeln:
1. Tests rufen **nur Workflow-Keywords** auf (Ausnahme: `tests/01_smoke`).
2. **Keine technischen Daten im Test** (keine Registeradressen, URLs, Selektoren).
3. **Keine Logik im Robot-Code:** Bedingungen, Schleifen über Daten, Umrechnungen und Toleranzen
   gehören in Python. Robot beschreibt, Python rechnet.
4. Kein `Sleep`; gewartet wird auf Zustände.

## Sprache und Namen

- Robot-Dateien: **Deutsch**. Python-Code und Library-Keywords: **Englisch**.
- Keyword-Namen: ein bis sechs Wörter, Form **Objekt + Verb im Infinitiv**
  (`Gerät hochfahren`, `Messwerte prüfen`). Einheitlich `prüfen`, `einstellen`, `abwarten`.
- Jedes Keyword hat `[Documentation]` mit einem Satz.

## Testdaten (`testdata/devices/*.json`)

Gegliedert nach Testdatenarten:

```json
{
  "device":      { "model": "MM-100", "variant": "A" },
  "environment": { "registers": { "setpoint_voltage": 40001, "measured_voltage": 30001,
                                  "temperature": 30002, "status": 30010 } },
  "control":     { "settle_timeout_s": 30, "repetitions": 3 },
  "measurement_points": [
    { "name": "MP1", "input": { "voltage_v": 5.0 },
      "expected": { "voltage_v": 5.0, "tolerance_v": 0.05, "max_temperature_c": 60 } }
  ]
}
```

Die Library lädt die Datei in Dataclasses (Werte-Objekte); fehlerhafte Dateien scheitern mit
verständlicher Meldung (Feld und Erwartung).

## Berichte

- `Metadata` in jeder Suite (Firmware, Seriennummer, Variante).
- Messwerte erscheinen im Log als **HTML-Tabelle** (Soll, Ist, Toleranz, Ergebnis).
- Fehlermeldungen sagen, was erwartet und was gefunden wurde.
- Fehler in der Vorbereitung brechen mit „Vorbereitung fehlgeschlagen: …“ ab.
- Teardown bringt das Gerät immer in einen sicheren Zustand.

## Arbeitsweise in Sessions

- Erst den Plan zeigen, dann umsetzen. Im Zweifel die einfachere Lösung.
- Kleine Commits mit deutschen Commit-Nachrichten.
- Am Ende Akzeptanzkriterien prüfen und `plan/HANDOFF.md` ergänzen.
- Ideen, die über den Auftrag hinausgehen, nicht bauen, sondern in `plan/LEUCHTTURM.md` notieren.
- Nichts außerhalb des Repos verändern, keine Geheimnisse einchecken.
