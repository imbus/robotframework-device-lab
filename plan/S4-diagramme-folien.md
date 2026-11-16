# S4 – Diagramme und Folien

**Ziel:** Eine schlanke Präsentation (ca. 25 Folien + 2 Joker) in der imbus-Vorlage, die
durch den Tag führt. Bilder statt Text; die meiste Zeit läuft VS Code.

**Arbeitsort:** Diagramme im Repo unter `docs/img/` (generisch, dürfen öffentlich sein).
Folien im Ordner `workshop-material/` **außerhalb** des Repos (Vorlage ist imbus-intern).
Kann parallel zu S1–S3 laufen; Screenshots kommen später als Platzhalter.

## Teil 1: Acht Diagramme (`docs/img/`, SVG + PNG 1920 px)

| Datei | Inhalt |
|---|---|
| `orchester` | Notenblatt = JSON, Dirigent = Robot Framework, Musiker = DeviceHub, Gerät, Browser, Aufnahme = Report/Log |
| `siedlung` | Fundament = Python-Libraries, drei Etagen = Keyword-Schichten, Wohnräume = Workflows, Bauplan = Doku, Bauordnung = robot.toml/Robocop, Leitungsnetz zwischen Häusern = zentrale Ressourcen |
| `landschaft` | JSON → Robot Framework → DeviceHub (REST) → Gerät; Browser → Web-UI; Report → Jenkins |
| `gtaa` | gTAA-Schichten mit den Projektbestandteilen |
| `schichten` | Workflow → Fachlich → Technisch → Library mit Beispiel-Keyword und den vier Regeln |
| `testdatenarten` | JSON-Ausschnitt farbig nach Eingabe, Soll, Steuerung, Umgebung |
| `fehlerkategorien` | Entscheidungsbaum Gerät, Test, Testdaten, Umgebung |
| `pipeline` | Robocop → pytest → Robot → Report, darunter „ein Befehl, drei Profile“ |

Stil: Farben der Vorlage – Grün `#00946C`, Dunkelblau `#005076`, Schiefer `#4C6369`,
Orange `#F69F00` (nur Hervorhebung), Hellgrün `#B3DFD3`, Blau `#4086C2`, Text `#5F5F5F`;
Calibri; flach, max. 7 Elemente pro Bild, auf dem Beamer lesbar.

## Teil 2: Folien

**Eingaben** in `workshop-material/`:
- `vorlage/imbus_vorlage.pptx` – **nur das Design übernehmen, keine Inhalte**
- `quellen/robot_framework_basics.pptx` – einzelne Folien als Vorlage, ins neue Design
  übertragen und an DeviceHub angepasst: 4/11 (Was RF ist), 22–27 (Suite-Struktur),
  32–36 (Report, Log, Status), 39 (User- vs. Library-Keywords), 80–83 (Best Practices, auf
  4 Regeln kürzen), 89–98 (Setup/Teardown, nur das Prinzip)
- `folienplan.csv` – Folienliste (wird auf ca. 25 Folien gekürzt, siehe unten)

**Vorlage (geprüft):** 16:9, Calibri. Layouts (Master 1, Namen exakt):
`1_Titelfolie Green imbus - 1-Zeilig`, `1_Agenda_green imbus`, `1_Kapiteltrenner Green imbus`,
`1_Zwei Inhalte, Bild rechts`, `1_Bild`, `1_Zwei Inhalte`, `1_3 Blöcke Inhalt`,
`1_Zitat green imbus`, `1_Kontakt green imbus`.

**Vorgehen:**
1. Vorlage mit python-pptx öffnen, alle vorhandenen Folien entfernen, Layouts behalten.
2. Pro Block: Kapiteltrenner mit der Kernbotschaft, dann 1–3 Folien, dann Live-Demo-Folie.
   Folien ohne eigenes Bild aus der Liste streichen oder zusammenlegen (Ziel ca. 25).
3. Titel als Aussage (max. 8 Wörter), höchstens 3 Stichpunkte à 6 Wörter oder nur ein Bild.
4. Live-Demo-Folien: Symbol + „Live in VS Code“ + ein Satz, was gleich passiert.
5. Sprechernotizen: 2–4 Sätze plus Übergang.
6. Fehlende Screenshots als grauer Platzhalter mit Dateinamen.
7. Ausgabe `workshop-material/folien/rf-workshop.pptx` + PDF-Vorschau.

## Akzeptanzkriterien

- [ ] Acht Diagramme als SVG und PNG, einheitlicher Stil
- [ ] Nur Layouts, Farben und Schriften der Vorlage
- [ ] Ca. 25 Folien, keine mit mehr als 25 Wörtern Fließtext
- [ ] Jede Folie hat Sprechernotizen
- [ ] Datei öffnet fehlerfrei in PowerPoint
