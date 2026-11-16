# S2 – Keyword-Schichten, Tests und Demo-Szenarien

**Ziel:** Das, was die Teilnehmenden sehen: lesbare Workflows in drei Schichten, ein
generischer Test für beide Varianten und vorbereitete Szenarien für die Live-Demos.

Voraussetzung: S1 ist fertig.

## Umfang

1. **Resources** nach den Schichtregeln aus CLAUDE.md:
   - `technisch/geraet.resource`, `technisch/register.resource`, `technisch/web_ui.resource`
   - `fachlich/geraet.resource` (`Gerät hochfahren`, `Gerät in sicheren Zustand bringen`),
     `fachlich/messung.resource` (`Messpunkt einstellen`, `Messwerte erhalten`, `Messwerte prüfen`)
   - `workflow/messung.resource` (`Messung durchführen`)
2. **Tests:**
   - `02_messung/messung_durchfuehren.robot`: **ein** generischer Test, Profil aus `robot.toml`;
     Suite-Setup setzt `Metadata`; Test-Teardown `Gerät in sicheren Zustand bringen`
   - `03_web_ui/statusseite.robot`: Gerät über die Web-Seite einschalten, Zustand prüfen
   - Tags: `smoke`, `messung`, `ui`
3. **Error-Handling:** Scheitert das Hochfahren, bricht der Test mit „Vorbereitung
   fehlgeschlagen: …“ ab, der Teardown läuft trotzdem.
4. **Quiz-Profile** in `robot.toml` (Fehler werden im Suite-Setup gesetzt):
   - `quiz-1`: Gerät hängt beim Einschwingen → Ursache **Gerät/Umgebung**
   - `quiz-2`: `testdata/quiz/falscher_sollwert.json` → Ursache **Testdaten**
   - `quiz-3`: Drift → Ursache **System unter Test**
   - Die Ursache muss im Log auffindbar sein, ohne dass die Meldung sie verrät.
5. **Anti-Pattern** `antipatterns/messung_antipattern.robot`: dieselbe Prüfung mit
   verschachteltem IF/FOR, `Sleep`, harten Registeradressen und Copy-Paste. Läuft grün,
   Kopfkommentar „Absichtlich schlecht – Demo“.
6. **`just reset`:** Fehler im Mock löschen, Geräte aus, `results/` leeren, nicht eingecheckte
   Dateien in `testdata/devices/` entfernen.

## Nicht bauen

Listener, Legacy-Seite, weitere Testsuiten.

## Akzeptanzkriterien

- [ ] `just test-a` und `just test-b` grün mit demselben Testcode
- [ ] Neue Datei `variante_c.json` (Kopie von B, andere Register) läuft ohne Codeänderung
- [ ] Im Log sind die drei Schichten beim Aufklappen klar erkennbar
- [ ] Die drei Quiz-Profile scheitern mit unterschiedlichen, nachvollziehbaren Meldungen
- [ ] Mock während eines Laufs stoppen → klarer Abbruch, Teardown versucht den Reset
- [ ] UI-Test grün (nach `uv run rfbrowser init`)
- [ ] Anti-Pattern läuft grün
