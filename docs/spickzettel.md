# Spickzettel Robot Framework

Vorderseite · Tests lesen, starten und bewerten

Robot Framework testet hier über REST ein simuliertes Messmodul MM-100 (Varianten A und B) im
Mock-Werkzeug DeviceHub. Der Test bleibt gleich, Registeradressen und Soll-Werte stehen je
Variante in einer JSON-Datei. Projekt: `robotframework-device-lab`, Start siehe `README.md`.

## Test starten

Vorher in einem eigenen Terminal den Mock starten: `just sim`. `just` allein listet alle Befehle.

| Was | VS Code mit RobotCode | Kommandozeile |
| ------ | ---------- | -------------- |
| Alle Tests | Testansicht (Kolben links) → ▶ | `just test` |
| Ein Test | „Run“ über dem Testnamen | `just test --test messwerte_im_toleranzband` |
| Anderes Gerät | Profil wählen: `RobotCode: Select Configuration Profiles` | `just test-b` |
| Nach Tag filtern | – | `just test --include smoke` |
| Trockenlauf | – | `just dryrun` (prüft Syntax und Keywords) |
| Neues Profil | – | `just test --variable GERAETEPROFIL:data/devices/variante_c.json` |

- `just test-b` ist kurz für `uv run robotcode --profile variante-b robot`. RobotCode liest Pfade,
  Variablen und Profile aus `robot.toml`, im Editor genauso wie in der Pipeline.
- Ohne RobotCode geht alles mit `robot`, dann aber jede Option von Hand:
  `robot --pythonpath .:src/libs --variable GERAETEPROFIL:data/devices/variante_b.json … tests`
- Optionen stehen **vor** dem Testpfad: `just test --include smoke tests/01_smoke`

## Ergebnisse lesen

| Datei | Wofür |
| ---- | ------------ |
| `results/report.html` | Überblick: grün oder rot, Statistik nach Tags, Metadaten (Firmware, Seriennummer, Variante) |
| `results/log.html` | jeder Schritt zum Aufklappen; unter „Messung durchführen“ die Messwert-Tabelle mit Soll, Ist, Toleranz und Ergebnis, Abweichungen rot |

**PASS** bestanden · **FAIL** gescheitert · **SKIP** bewusst übersprungen.
Im Terminal: `uv run robotcode results summary` (Zahlen), `… results show` (Fehlermeldungen), `… results log` (Schritte).

## Fehlerkategorien: Wo es rot wird, verrät die Ursache

| Rot in … | Meldung (Beispiel) | Ursache |
| ------- | ---------- | ----- |
| Setup `Prüfstand vorbereiten` | „Geräteprofil … fehlerhaft: Feld … fehlt – erwartet: …“ | **Testdaten** |
| Setup `Prüfstand vorbereiten` | „DeviceHub unter … nicht erreichbar. Läuft der Mock (just sim)?“ | **Umgebung** |
| Setup `Gerät hochfahren` | „… READY nicht innerhalb von 15 s erreicht. Letzter Zustand: …“ | **Gerät / Umgebung** |
| ein Schritt im Test | „No keyword with name … found“, falscher Ablauf | **Test** |
| `Spannungen prüfen`, Abweichung konstant | „MP1 Messung 1: erwartet 5.500 V ± 0.050 V, gemessen 4.995 V“ | **Testdaten** (Soll falsch) |
| `Spannungen prüfen`, Abweichung wächst | erst in Ordnung, dann immer weiter daneben | **Gerät** (Drift) |

Robot meldet Fehler im Setup als „Setup failed: …“. Der Teardown `Gerät in sicheren Zustand bringen`
läuft immer, auch nach einem Fehler; scheitert er auch, steht „Also teardown failed“ darunter.

## Debuggen in RobotCode in drei Schritten

1. **Haltepunkt setzen:** links neben die Zeilennummer klicken (roter Punkt), z. B. bei `Messergebnis bewerten`.
2. **Im Debugger starten:** „Debug“ über dem Testnamen. Der Lauf hält am Haltepunkt an.
3. **Werte ansehen, weiterlaufen:** links unter „Variablen“ steht z. B. `${messwerte}`.
   F10 nächster Schritt, F11 in das Keyword hinein, F5 weiter bis zum Ende.

<div class="rueckseite"></div>

# Tests bauen, die bleiben

Rückseite · Schichten, Testdaten und Begriffe aus QF-Test

## Die Schichten: Wer ruft wen?

| Schicht | Ordner | Beispiel |
| --------- | -------- | ----------- |
| Test | `tests/` | `Messwerte im Toleranzband` |
| Workflow: ganze Abläufe | `src/resources/workflow/` | `Messung durchführen`, `Messergebnis bewerten` |
| Fachlich: einzelne Schritte | `src/resources/fachlich/` | `Gerät hochfahren`, `Spannungen prüfen` |
| Technisch: Python-Library, Browser Library | `src/libs/DeviceHubLibrary/` | `Run Measurement Group`, `Write Register` |

## Die vier Regeln

1. **Tests rufen nur Workflow-Keywords auf.** Setup und Teardown dürfen fachliche Keywords nutzen,
   der Smoke-Test ist die Ausnahme.
2. **Keine technischen Daten im Test:** keine Registeradressen, URLs oder Selektoren.
   Die stehen im JSON (`data/`), in `robot.toml` oder ganz unten in der Library.
3. **Keine Logik im Robot-Code:** keine Bedingungen, Schleifen, Umrechnungen oder Toleranzen.
   Robot beschreibt, Python rechnet.
4. **Kein `Sleep`:** Gewartet wird auf einen Zustand, z. B. `Wait Until Device State Is    READY`.

**Namen:** Objekt + Verb im Infinitiv (`Gerät hochfahren`, `Spannungen prüfen`), ein bis sechs Wörter.
Robot-Dateien deutsch, Python englisch. Jedes Keyword hat einen Satz `[Documentation]`.
Prüfen mit `just lint` (Robocop).

## Testdaten: ein JSON je Gerät

| Abschnitt | Testdatenart | Inhalt |
| ----- | ----- | ------------ |
| `device` | Gerät | Modell und Variante |
| `environment` | Umgebung | Registeradressen |
| `control` | Steuerung | Timeout, Wiederholungen |
| `measurement_points` | Eingabe und Erwartung | Eingangsspannung, Soll, Toleranz, Temperaturgrenze je Messpunkt |

Neues Gerät: JSON kopieren, Werte anpassen, mit `--variable GERAETEPROFIL:…` starten. Kein neuer Testcode.

## Aus QF-Test bekannt

| QF-Test | Robot Framework | Bei uns |
| ------- | ------ | ---------- |
| Testsuite | Suite-Datei (`.robot`) | `tests/02_messung/messung_durchfuehren.robot` |
| Testfallsatz | Ordner | `tests/02_messung/` |
| Prozedur | Keyword | `Messung durchführen` |
| Package | Resource-Datei (`.resource`) | `src/resources/workflow/messung.resource` |
| Variablen | Variablen | `${GERAETEPROFIL}`, Profile in `robot.toml` |
| Abhängigkeit, Vorbereitung, Aufräumen | Setup und Teardown | `Gerät hochfahren`, `Gerät in sicheren Zustand bringen` |
| Datentreiber | Werte-Objekte aus JSON | `data/devices/variante_a.json` |
| Check | Prüf-Keyword | `Spannungen prüfen` |
| Skript (Jython, Groovy) | Python-Library | `src/libs/DeviceHubLibrary/` |
| Protokoll | `log.html` (Überblick: `report.html`) | `results/` |

## Mehr

- Alle Befehle: `just` · Keyword-Doku erzeugen: `just docs` (nach `docs/keywords/`)
- Robot Framework: <https://robotframework.org> · RobotCode: <https://robotcode.io>
