# S5 – Spickzettel und Drehbuch

**Ziel:** Das Blatt zum Mitnehmen und das Drehbuch, mit dem der Tag sicher läuft.

Voraussetzung: S2 ist fertig (Befehle und Quiz-Profile stehen fest).

## Umfang

1. **Spickzettel** (im Repo: `docs/spickzettel.md` + PDF, eine A4-Seite, Vorder- und Rückseite):
   - Vorne: Workflow starten (Editor, Kommandozeile, Profil, Tag, Dry-Run), Log lesen,
     Fehlerkategorien, Debuggen in RobotCode in drei Schritten
   - Hinten: die vier Schichtregeln und QF-Test → Robot Framework als Kurztabelle
     (Testsuite → Suite-Datei, Testfallsatz → Ordner, Prozedur → Keyword, Package → Resource,
     Variablen → Variablen, Abhängigkeit/Vorbereitung/Aufräumen → Setup/Teardown,
     Datentreiber → Werte-Objekte aus JSON, Check → Prüf-Keyword, Skript → Python-Library,
     Protokoll → log.html)
2. **Drehbuch** (`workshop-material/drehbuch.md`, außerhalb des Repos):
   - Je Block: Minuten, Kernsatz, Demo-Schritte mit exakten Befehlen, erwartete Ausgabe,
     Fallback (Screencast-Datei), Übergangssatz, eine Umfrage- oder Quizfrage
   - Ratespiel-Schritte für Block 2, Lösungen zu `quiz-1` bis `quiz-3`
   - Checkliste für 30 Minuten vor Beginn

## Akzeptanzkriterien

- [ ] Spickzettel passt auf ein Blatt und ist ohne Workshop verständlich
- [ ] Jeder Befehl im Drehbuch wurde einmal im Repo ausgeführt
- [ ] Jede Live-Demo hat einen benannten Fallback
