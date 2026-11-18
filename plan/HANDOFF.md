# Übergaben zwischen den Sessions

Jede Session ergänzt hier einen Abschnitt.

## Vorlage

### S? – Titel (Datum)
- **Gebaut:**
- **Starten mit:**
- **Abweichungen vom Auftrag:**
- **Offen / Hinweise für die nächste Session:**

### S4 – Diagramme und Folien (18.11.2026)

- **Gebaut:**
  - Folien außerhalb des Repos in `workshop-material/folien/`: `rf-workshop.pptx` (26 Folien + 2 Joker)
    und `rf-workshop.pdf` als Vorschau, erzeugt von `erzeuge_folien.py` aus der Vorlage
    (alle Vorlagenfolien entfernt, nur Layouts der Vorlage).
  - Live-Demo-Folien im Layout `1_Zitat green imbus`: Play-Symbol, „Live in VS Code“, ein Satz,
    Block im Reiter. Jede Folie hat eine Sprechernotiz (2–4 Sätze + „Übergang: …“).
  - Das Skript prüft bei jedem Lauf: Fließtext ≤ 25 Wörter, Titel ≤ 8 Wörter, Notiz mit Übergang,
    nur Layouts, Schriften und Farben der Vorlage. Fehlende Bilder → grauer Platzhalter mit Dateiname.
  - Diagramme: nicht in dieser Session gebaut, sondern parallel in der S1-Session (`docs/img/`,
    8 × SVG + PNG, 1920 × 900). Die Folien binden `docs/img/*.png` ein.
- **Starten mit:** in `workshop-material/folien/`:
  `uv run --no-project --with python-pptx python erzeuge_folien.py --pdf`
  (PDF über PowerPoint per AppleScript; ohne `--pdf` nur PPTX + Prüfung).
- **Abweichungen vom Auftrag:**
  - Kein Kapiteltrenner pro Block (ergäbe ca. 35 Folien): Der Blockname steht als Unterzeile unter
    jedem Titel, nur der Nachmittag beginnt mit einem Kapiteltrenner (Entscheidung des Nutzers).
  - Gestrichen: „QF-Test → Robot Framework“ (reine Textfolie, steht auf dem Spickzettel).
    Titelfolie ohne Orchester-Bild (Vorlagenhintergrund), das Orchester steht auf Folie 3 und 13.
  - Zusätzlich genutzte Vorlagen-Layouts: `1_Titel und Inhalt` (Diagramm mit Titel) und
    `1_4 Kacheln/Blöcke` (Spielregeln). `1_Bild` nicht genutzt, weil es keinen Titel hat.
  - Titel aus `folienplan.csv` teils zu Aussagen umformuliert (z. B. „Jede Testdatei hat feste Abschnitte“).
  - Diagramme setzen Code-Bezeichner in Consolas/Menlo, alles andere in Calibri (gewollt: Code in Monospace).
- **Offen / Hinweise für die nächste Session:**
  - Screenshots fehlen noch: `folien/screenshots/` mit `anatomie_testdatei.png`, `report.png`,
    `log_messwerte.png`, `log_vorher.png`, `log_nachher.png` füllen, dann das Skript erneut starten.
  - Nach S2/S3 abgleichen: Beispielcode auf Folie 18 mit `antipatterns/messung_antipattern.robot`,
    Befehle auf Folie 8 und in den Live-Notizen (`just lint`, Quiz-Profile `quiz-1` bis `quiz-3`).
  - Fachlich prüfen: Pilotkarten S/M/L (Folie 25) und KI-Joker (Folien 27–28).
  - Klassifizierung (ISK) auf der Titelfolie ist bewusst leer.
  - Ändern sich Diagramme in `docs/img/`, die Folien einfach neu erzeugen.

### S1 – Mock-Gerät, Library, Testdaten, robot.toml (18.11.2026)

- **Gebaut:**
  - Gerüst: `pyproject.toml` (uv, Python 3.14, Versionen in `uv.lock`), `justfile` (`sim`, `test`, `test-a`, `test-b`, `dryrun`), `.gitignore`, `LICENSE` (MIT), leere Schichtordner in `resources/`.
  - Mock `devicehub/` (FastAPI): Geräte `mm100-a` und `mm100-b`, Zustände `OFF → BOOTING → SETTLING → READY → MEASURING → READY` plus `FAULT` (Eingangsspannung über Gerätelimit), Fehler `hang`/`drift`/`disconnect` über `POST`/`DELETE /sim/faults`, Statusseite `/ui/devices/{id}` mit `data-testid`, `/docs` offline (`fastapi-offline`).
  - `libraries/DeviceHubLibrary/`: `model.py` (Werte-Objekte), `profile.py` (JSON laden und prüfen), `checks.py` (Toleranz, HTML-Tabelle), `client.py` (REST), `__init__.py` (Keywords, deutsche Docstrings).
  - Testdaten `testdata/devices/variante_a.json` und `variante_b.json`, `robot.toml` mit Standard (= A), `variante-a`, `variante-b`, `ci`.
  - Unit-Tests `libraries/tests/` (Profil laden, fehlerhaftes Profil, Toleranzprüfung) und Smoke-Test `tests/01_smoke/geraet_erreichbar.robot`.
  - S4 Teil 1 parallel: acht Diagramme in `docs/img/` (SVG + PNG 1920 × 900).
- **Starten mit:** `uv sync`, dann `just sim` (Terminal 1) und `just test-a` / `just test-b` (Terminal 2); `uv run pytest`.
- **Abweichungen vom Auftrag:**
  - Python 3.14 statt 3.12 (Entscheidung des Nutzers; CLAUDE.md und S3 angepasst).
  - `settle_timeout_s` 15 statt 30, damit das Hänge-Quiz nicht 30 s stumm wartet.
  - Zusätzliche Abhängigkeit `fastapi-offline`, damit `/docs` ohne Internet funktioniert.
  - Konfiguration in `pyproject.toml`: Robocop prüft deutsche Keyword-Namen mit `first_word_capitalized` („Gerät hochfahren“), Mypy findet die Library (`mypy_path`), Ruff duldet den RF-üblichen Paketnamen `DeviceHubLibrary` (N999).
  - KISS-Schnitt auf Wunsch des Nutzers: kein `GET /sim/faults`, keine Startmeldung, Statusseite nur mit Zustand, Messwert und Ein/Aus. Die Profilprüfung meldet Tippfehler als „Feld … fehlt“, statt unbekannte Felder extra zu prüfen.
  - Drei statt zwei pytest-Funktionen (fehlerhaftes Profil als eigener Test).
  - Nach dem Code-Review:
    - Temperaturregister 30003/31003, weil ein float32-Messwert zwei Modbus-Register belegt.
    - Toleranzen einheitlich 1 % der Erwartung.
    - „Eingangsspannung“ für die Vorgabe, „Soll“ nur für die Erwartung.
    - Code höchstens 100 Zeichen pro Zeile (Beamer).
  - Claude committet nicht; der Nutzer committet selbst.
- **Offen / Hinweise für die nächste Session:**
  - **Entscheidung vor S2:** `Run Measurement Group` läuft in Python über alle Messpunkte (Regel 3: keine Schleifen über Daten im Robot-Code). Damit hat `Messpunkt einstellen` (CLAUDE.md, Diagramm `schichten`) keinen Platz im Messablauf. Entweder bleibt das so und S2 nutzt `Messwerte erhalten` / `Messwerte prüfen`, oder Regel 3 erlaubt genau eine Schleife im Workflow über die Messpunkte; dann misst die Library je Punkt. Der Plan-Review empfiehlt Option A (bleibt in Python): Die Library bleibt unverändert, und Folie 18 zeigt die Robot-Schleife schon als Anti-Pattern.
  - Für die Quiz-Profile braucht S2 einen Weg, Fehler ein- und auszuschalten (`POST`/`DELETE /sim/faults`), als Keyword oder als `just`-Rezept.
  - `variante_c.json`: Der Mock kennt nur A und B. Für das S2-Kriterium braucht er ein drittes Gerät (ein Eintrag in `DEVICE_SPECS`, z. B. 42001/32001/32003/32010, Spannungsgrenze ≥ 110 V). Eine beliebige JSON-Datei startet man mit `just test --variable GERAETEPROFIL:…`.
  - Die Quiz-Datei nicht `falscher_sollwert.json` nennen: Der Pfad steht im Log und verrät die Lösung.
  - Das Anti-Pattern von Folie 18 nutzt Adressen (`Write Register 40001`), die Library erwartet aber Registernamen.
  - Meldungen für die Quiz-Auflösung: Hängen → „… nicht innerhalb von 15 s erreicht. Letzter Zustand: SETTLING.“; Drift → erster Wert in Ordnung, danach wachsende Abweichung (unterscheidbar vom konstanten Versatz bei falschen Testdaten).
  - Mock gestoppt → „DeviceHub unter … nicht erreichbar … Läuft der Mock (just sim)?“; `Reset Device To Safe State` versucht den Reset und scheitert mit derselben Meldung.
  - Für S3 (Jenkins/Docker): Mock im Container mit `--host 0.0.0.0` starten, URL über `DEVICEHUB_URL` setzen.
  - VS Code muss die Projektumgebung nutzen („Python: Interpreter auswählen“ → `.venv/bin/python`), sonst finden Pylance und RobotCode Robot Framework und die Library nicht.
