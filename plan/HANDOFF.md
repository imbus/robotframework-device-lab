# Übergaben zwischen den Sessions

Jede Session ergänzt hier einen Abschnitt.

## Vorlage

### S? – Titel (Datum)
- **Gebaut:**
- **Starten mit:**
- **Abweichungen vom Auftrag:**
- **Offen / Hinweise für die nächste Session:**

### S2 – Keyword-Schichten, Tests, Demo-Szenarien (18.11.2026)

- **Gebaut:**
  - Neues Layout (Wunsch des Nutzers): `src/resources/{workflow,fachlich}/`, `src/libs/DeviceHubLibrary/`
    (+ `src/libs/tests/`), Testdaten in `data/`, Anti-Pattern in `tests/antipatterns/`.
    Imports ohne `../`: `Resource    src/resources/…`, dafür `python-path = [".", "src/libs"]` in `robot.toml`.
  - **Schichten:** Workflow (Robot) → Fachlich (Robot) → Technisch = Python-Library bzw. Browser.
    Es gibt keine `technisch/`-Resources mehr (Entscheidung des Nutzers: 1:1-Umbenennungen waren eine
    Schicht zu viel). Jede Resource hat `Keyword Tags workflow|fachlich`, im Log beim Aufklappen sichtbar.

    | Schicht | Datei | Keywords |
    |---|---|---|
    | Test | `tests/02_messung/messung_durchfuehren.robot` | `Messwerte im Toleranzband` |
    | Workflow | `src/resources/workflow/messung.resource` | `Messung durchführen` (liefert `${messwerte}`), `Messergebnis bewerten` |
    | Fachlich | `src/resources/fachlich/messung.resource` | `Messwerte erhalten`, `Messprotokoll erstellen`, `Spannungen prüfen`, `Temperaturen prüfen` |
    | Fachlich | `src/resources/fachlich/geraet.resource` | `Prüfstand vorbereiten` (Suite-Setup), `Gerät hochfahren` (Test-Setup), `Gerät in sicheren Zustand bringen` (Test-Teardown) |
    | Workflow | `src/resources/workflow/statusseite.resource` | `Gerät über Statusseite in Betrieb nehmen` |
    | Fachlich | `src/resources/fachlich/statusseite.resource` | `Gerät über Statusseite einschalten`, `Angezeigte Betriebsbereitschaft prüfen` |
    | Python | `DeviceHubLibrary` | `Run Measurement Group`, `Log Readings Table`, `Voltages Should Be Within Tolerance`, `Temperatures Should Stay Below Limit`, … |

  - Library: `Readings Should Match Expectation` aufgeteilt in `Log Readings Table`,
    `Voltages Should Be Within Tolerance`, `Temperatures Should Stay Below Limit` (damit Test und Workflow
    mehrere Schritte haben). Neu `Set Simulated Fault`; `Write/Read Register` nehmen auch eine Adresse
    („40001“) für das Anti-Pattern. httpx-Logger auf WARNING, sonst stand jede HTTP-Anfrage im Robot-Log.
  - Mock: Variante C (`mm100-c`, 42001/32001/32003/32010, 250 V) und `POST /sim/reset`.
  - Tests: `02_messung` (ein generischer Test, Tag `messung`), `03_web_ui/statusseite.robot` (Tag `ui`,
    Browser sichtbar; unsichtbar mit `--variable HEADLESS:True`).
  - Quiz-Profile `quiz-1..3` in `robot.toml` (nur `tests/02_messung`), Fehler setzt das Suite-Setup über
    `${SIMULATIONSFEHLER}`; jedes normale Suite-Setup löscht alle Fehler wieder.
  - `just quiz <n>`, `just antipattern`, `just reset`. Robocop: `sleep-keyword-used` eingeschaltet.
- **Starten mit:** `just sim`, dann `just test-a` / `just test-b` / `just quiz 1` / `just antipattern`.
  Einmalig für den UI-Test: `uv run rfbrowser init chromium` (in dieser Session gelaufen).
  Neues Gerät: Kopie von `variante_b.json` als `data/devices/variante_c.json` (Variante C, Register 42001 …),
  dann `just test --variable GERAETEPROFIL:data/devices/variante_c.json`.
- **Quiz-Auflösung (nicht auf Folien zeigen):**
  - `quiz-1` Fehler `hang` → **Gerät/Umgebung**: „Setup failed: … READY nicht innerhalb von 15 s erreicht.
    Letzter Zustand: SETTLING.“
  - `quiz-2` `data/quiz/quiz_2.json`, MP1 Soll 5,5 V statt 5,0 V → **Testdaten**: nur MP1, konstant ca. 0,5 V daneben.
  - `quiz-3` Fehler `drift` → **System unter Test**: MP1 Messung 1 in Ordnung, danach wachsende Abweichung (8 von 9).
  - Im Log steht der Fehler als Argument von `Set Simulated Fault` im Suite-Setup (= Auflösung beim Aufklappen).
- **Akzeptanzkriterien:** alle geprüft und erfüllt. A und B grün mit demselben Testcode; Variante C ohne
  Codeänderung grün; Schichten im Log erkennbar (`uv run robotcode results log`); Quiz 1–3 mit
  unterschiedlichen Meldungen; Mock gestoppt → „DeviceHub … nicht erreichbar … Läuft der Mock (just sim)?“
  und „Also teardown failed“ mit Reset-Versuch; UI-Test grün; Anti-Pattern grün (ca. 25 s).
- **Abweichungen vom Auftrag:**
  - Keine technische Resource-Schicht, kein `Messpunkt einstellen`, kein `register.resource` (Option A).
  - Kein „Vorbereitung fehlgeschlagen: …“: `Gerät hochfahren` liegt im Test-Setup ohne TRY, Robot meldet
    „Setup failed: …“ (Entscheidung des Nutzers). Setup und Teardown rufen fachliche Keywords direkt auf.
  - Quiz-Datei `data/quiz/quiz_2.json` statt `falscher_sollwert.json` (Name verriet die Lösung).
  - Anti-Pattern mit zwei kopierten Tests (A und B) statt einem; hat keine Settings-Doku (gewollt).
- **Offen / Hinweise für die nächste Session:**
  - **CLAUDE.md ist nicht angepasst** (Vorschlag an den Nutzer): Ordner `src/resources`, `src/libs`, `data/`;
    Schichten-Tabelle ohne `resources/technisch/`; Regel „Vorbereitung fehlgeschlagen“ → „Setup failed“;
    Varianten A, B und C.
  - `just reset` löscht neue Profile per `git clean` und bricht ab, solange `data/devices/` nicht eingecheckt ist.
    In dieser Session hat ein Reset vor dieser Sicherung `variante_a/b.json` gelöscht; beide sind aus HEAD
    (`testdata/devices/`) wiederhergestellt.
  - Anti-Pattern hat `Test Tags antipattern` und ist in `robot.toml` per `excludes` ausgeschlossen; nur
    `just antipattern` (Profil `antipattern` mit `excludes = []`) führt es aus. Robocop auf `tests/` zeigt
    dessen Befunde weiterhin (gewollt für die Robocop-Razzia).
  - Behoben: Profil `ci` nutzte `extend-exclude` (ungültig, von RobotCode still ignoriert → UI-Test lief in
    CI mit). Richtig ist `extend-excludes`; geprüft mit `robotcode --profile ci discover tests`.
  - Folien/Diagramme (S4): Kette jetzt Test → `Messung durchführen` + `Messergebnis bewerten` → fachlich →
    Python; Folie 18 und Anti-Pattern-Code (`Write Register 40001`, `Sleep 6s/2s`) abgleichen.

### S3 – Robocop, README, Jenkins minimal (19.11.2026)

- **Gebaut:**
  - `just lint` (`robocop check`, Befunde nur in `tests/04_antipatterns`), `just format`
    (`robocop format --exclude tests/04_antipatterns`, damit das Anti-Pattern schlecht bleibt).
  - `just setup` (`uv sync` + `rfbrowser install chromium`), `just docs` (LibDoc über `robotcode libdoc`
    für Library und alle Resources nach `docs/keywords/`, per `.gitignore` ausgeschlossen).
  - `README.md`: ein Satz, Voraussetzungen, Start in drei Befehlen, Befehlstabelle, Ordner, vier Regeln.
  - **Browser Batteries** (`robotframework-browser-batteries`, Wunsch des Nutzers): bringt Node.js mit,
    Node.js ist keine Voraussetzung mehr (lokal und in Jenkins). Browser kommen mit `rfbrowser install`.
  - Jenkins: `docker-compose.yml` (Jenkins auf `127.0.0.1:8081` + Mock-Container `devicehub`, Repo als
    `/repo:ro`), `jenkins/Dockerfile` (Jenkins 2.580.2 LTS + uv; venv aus `uv.lock` unter `/opt/venv` mit
    Chromium und dessen Systembibliotheken fest im Image; Plugins `workflow-aggregator`, `git`, `robot`),
    `.dockerignore` (Image bekommt nur `pyproject.toml` und `uv.lock`), `devicehub/Dockerfile`,
    `Jenkinsfile` (Lint → Unit → Robot, Robot-Plugin im `post` der Robot-Stage),
    `jenkins/EINRICHTUNG.md` (9 Schritte). Profil `ci`: `DEVICEHUB_URL=http://devicehub:8080`,
    `HEADLESS=True`, **UI-Test läuft mit** (Wunsch des Nutzers).
  - Ohne Einrichtungsassistent und Anmeldung (nur lokal gebunden), lokaler Git-Checkout erlaubt,
    CSP aus, damit `log.html` in Jenkins angezeigt wird (alles über `JAVA_OPTS` in Compose).
- **Starten mit:** `just jenkins`, dann `jenkins/EINRICHTUNG.md`; stoppen mit `just jenkins-stop`.
- **Akzeptanzkriterien:**
  - `just lint`: 9 Befunde, alle in `tests/04_antipatterns` ✔
  - Frischer Klon (Scratchpad, Arbeitsstand dort committet): `just setup`, `just test` 3/3 grün, `just docs` ✔
    (`just sim` nicht im Klon gestartet, weil der Mock auf 8080 schon lief)
  - Jenkins-Lauf grün in 21 s (Lint ohne Befunde, 7 Unit-Tests, 3 Robot-Tests inkl. Web-UI), Robot Results
    und `log.html` im Job sichtbar ✔ (Job per REST mit den Einstellungen der Anleitung auf einen
    Scratchpad-Klon mit committetem Arbeitsstand, danach gelöscht)
  - WLAN aus: gestrichen (Entscheidung des Nutzers, WLAN vor Ort)
- **Abweichungen vom Auftrag:**
  - Kein `just offline-prepare` (steht in `LEUCHTTURM.md`). Weil alles im Jenkins-Image liegt, braucht
    nur `just jenkins` beim ersten Bauen oder nach Änderung von `uv.lock` Internet.
  - Docker Desktop statt Rancher Desktop (auf dem Vorführ-Laptop installiert); Compose läuft mit beiden.
  - Smoke-Test und `geraet.resource` hat der Nutzer selbst umgebaut (`Gerätedaten bereitstellen`,
    `[Metadata]` am Test, `# robocop: off=no-suite-variable`).
- **Offen / Hinweise für die nächste Session:**
  - Jenkins baut nur **committete** Stände des eingetragenen Branches (Anleitung: `*/main`);
    vor der Demo committen. Jenkins liest das lokale `.git`, ein Push ist dafür nicht nötig.
  - Vor dem Workshop einmal `just jenkins` + Build laufen lassen (Images und uv-Cache warm), danach kein
    `docker compose down -v` und kein `docker system prune`.
  - Jenkins-Image: 1,98 GB, erster Bau dauerte bei langsamer Verbindung ca. 40 Minuten (Chromium und
    Systembibliotheken). Stolperstein: Das Node aus den Batteries braucht `libatomic1`; fehlt es, endet
    `rfbrowser install` trotzdem mit Exit-Code 0 und der UI-Test scheitert erst in Jenkins mit
    „Could not connect to the playwright process“ (Ursache in `results/playwright-log.txt`).
  - `just format` einmal über alle Dateien gelaufen (Settings-Spalte 17 statt 20). In `.vscode/settings.json`
    ist Robocop für RobotCode aus; formatiert VS Code anders, wechseln sich beide ab.
  - S4: `just lint` und Jenkins in den Notizen der Folien 23–25 abgleichen.
  - CLAUDE.md weiterhin nicht an S2 angepasst (siehe S2).

### S4 – Diagramme und Folien (18.11.2026)

- **Gebaut:**
  - Folien außerhalb des Repos in `workshop-material/folien/`: `rf-workshop.pptx` (29 Folien + 1 Joker)
    und `rf-workshop.pdf` als Vorschau, erzeugt von `erzeuge_folien.py` aus der Vorlage
    (alle Vorlagenfolien entfernt, nur Layouts der Vorlage, Metadaten der Vorlage neutralisiert).
  - Live-Demo-Folien im Layout `1_Zitat green imbus`: Play-Symbol, „Live in VS Code“, ein Satz,
    Block im Reiter. Jede Folie hat eine Sprechernotiz (2–4 Sätze + „Übergang: …“).
  - Das Skript prüft bei jedem Lauf: Fließtext ≤ 25 Wörter (ohne Überschriften, Reiter und Code),
    Titel ≤ 8 Wörter und ≤ 50 Zeichen, Notiz mit Übergang, nur Layouts, Schriften und Farben der Vorlage
    (plus Consolas für Code). Fehlende Bilder → grauer Platzhalter mit Dateiname.
  - Diagramme in `docs/img/` (8 × SVG + PNG, 1920 × 900): ursprünglich aus der S1-Session; nach dem
    Folien-Feedback in S4 neu gezeichnet: `schichten` (ein Schritt von fachlich bis technisch,
    allgemeine Regeln), `fehlerkategorien` (Log-Baum: wo es scheitert, verrät die Ursache),
    `pipeline` (CI-Best-Practices), in `gtaa` „Profile je Gerät“ statt „3 Profile“.
  - Klassische gTAA-Abbildung (ISTQB) aus dem Basis-Foliensatz in `workshop-material/folien/bilder/`.
- **Starten mit:** in `workshop-material/folien/`:
  `uv run --no-project --with python-pptx python erzeuge_folien.py --pdf`
  (PDF über PowerPoint per AppleScript aus einer Kopie, damit eine offene Fassung nicht stört).
- **Abweichungen vom Auftrag:**
  - Kein Kapiteltrenner pro Block: Der Blockname steht als Unterzeile unter jedem Titel, nur der
    Nachmittag beginnt mit einem Kapiteltrenner (Entscheidung des Nutzers).
  - 29 + 1 statt ca. 25 + 2 Folien: Nach dem Feedback des Nutzers kamen „Was RF ist und was nicht“,
    die klassische gTAA und eine Anti-Pattern-Übersicht dazu; das Orchester steckt nur noch in Titel
    und Notiz der Landschaftsfolie; die beiden KI-Joker sind zu einem zusammengelegt.
  - Gestrichen: „QF-Test → Robot Framework“ (reine Textfolie, steht auf dem Spickzettel).
  - Code auf Folien und in Diagrammen in Consolas (Entscheidung des Nutzers), sonst Calibri.
  - Zusätzlich genutzte Vorlagen-Layouts: `1_Titel und Inhalt`, `1_4 Kacheln/Blöcke`,
    `1_6 Kacheln/Blöcke`. `1_Bild` nicht genutzt, weil es keinen Titel hat.
- **Offen / Hinweise für die nächste Session:**
  - Screenshots eingebaut (22.11.): alle fünf aus `folien/screenshots/`, keine Platzhalter mehr.
    Bildunterschrift Folie 22 jetzt „Vorher: nur „Messwert falsch““ / „Nachher: Messpunkt, Soll, Ist,
    Toleranz“, Notiz dazu nach Anti-Pattern und `just quiz 2`. Notizen Folie 24 (Pre-Commit als
    Empfehlung, im Lab nur `just lint` + Jenkins) und 26 (9 Befunde in `tests/04_antipatterns`, Jenkins
    auf localhost:8081, ca. 20 s, Screencast als Rückfall) an S3 angepasst.
  - `log_vorher.png` und `log_nachher.png` am 22.11. als Ausschnitte neu aufgenommen: kein lokaler Pfad
    mehr, auf der Folie lesbar. Alle fünf Screenshots sind ohne Pfad, Benutzer- und Kundennamen geprüft.
  - Messwert-Tabelle im Log war im dunklen Log-Design kaum lesbar (hellgraue Schrift auf hellgrünem Grund).
    Behoben am 22.11. auf Wunsch des Nutzers: `_CELL` in `src/libs/DeviceHubLibrary/checks.py` setzt
    `color:#1f1f1f`, Abweichungen bleiben rot. `log_messwerte.png` neu aufgenommen, Folien neu erzeugt.
  - An S2 angeglichen (18.11.): Diagramme `schichten`, `fehlerkategorien`, `siedlung`, `gtaa` ohne
    technische Resource-Schicht (Workflow → Fachlich → Python) und mit den neuen Ordnern; Folie 8
    (`robot --pythonpath .:src/libs … tests/02_messung`, gegen einen Mock geprüft), Folie 13 und 20
    (Code aus `tests/02_messung` und `tests/antipatterns`), Notizen zu Quiz, Variante C, Stecker ziehen.
  - Neu in Block 8 (22.11., Wunsch des Nutzers): Folie 23 „Die Messwert-Tabelle ist HTML, kein Bild“ –
    Python-Code (`Log Readings Table`, `logger.info(html, html=True)`, leicht vereinfacht) neben dem
    HTML, das in `log.html` ankommt. Ab hier verschieben sich die Foliennummern um eins.
  - Fachlich prüfen: Pilotkarten S/M/L (Folie 28) und KI-Joker (Folie 30).
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

### Beispiele – Botschaft und Vorhersage in vorhandenen Tests (18.11.2026)

- **Gebaut:** kein Ordner `beispiele/`. Das Kontrastpaar „Einzelschritte wie heute ↔ Prüfvorschrift“
  tragen schon `tests/antipatterns/messung_antipattern.robot` und `tests/02_messung/messung_durchfuehren.robot`.
  - Beide Dateien beginnen mit `*** Comments ***`: Botschaft in einem Satz und Vorhersage-Frage für den Trainer.
  - `02_messung`: Am Test stehen `[Metadata]` Anforderung (REQ-MM100-012) und Prüfvorschrift (RF 7.5).
    Sie erscheinen im Log als eigene Zeilen neben den Suite-Metadaten.
    Dazu ein Kommentarsatz zu den QF-Test-Begriffen (Vorbereitung → Setup, Aufräumen → Teardown, Prozedur → Keyword).
- **Starten mit:** `just sim`, dann `just test-a` (Messung) und `just antipattern` (läuft grün).
- **Abweichungen vom Auftrag:**
  - Statt drei neuer Dateien keine neue Datei, auf Wunsch des Nutzers. Weggelassenes steht in `plan/LEUCHTTURM.md`.
  - Kein `[Metadata]` für Messpunkte: Der Test ist für alle Varianten gleich, die Messpunkte stehen im Profil.
  - Kein `just beispiele`.
- **Offen:** Die Diagramme `schichten`, `fehlerkategorien`, `siedlung` und `gtaa` zeigen noch eine technische
  Resource-Schicht. Seit S2 ist die Python-Library die technische Schicht. Der Auftrag für die Folien-Session
  liegt beim Nutzer.
