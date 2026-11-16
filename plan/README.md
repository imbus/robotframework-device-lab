# Arbeitsplan: Sessions für Claude Code

Jede Datei `S*.md` ist ein Auftrag für **eine** Claude-Code-Session.
`CLAUDE.md` im Wurzelverzeichnis liefert allen Sessions denselben Kontext.
Leitlinie: **Workshop zuerst**, alles Weitere steht in `LEUCHTTURM.md`.

## So startest du eine Session

```bash
cd rf-device-lab
claude
```

Prompt:

> Lies CLAUDE.md und plan/S1-mock-library.md. Zeig mir zuerst deinen Plan.
> Setz ihn dann um, prüf alle Akzeptanzkriterien und ergänze plan/HANDOFF.md.

Danach: Kriterien kurz selbst prüfen, committen, Tag `s1-done`.

## Sessions und Reihenfolge

| Session | Inhalt | Tag | Voraussetzung |
|---|---|---|---|
| **S1** | Mock-Gerät, Library, Testdaten, robot.toml | Di 17.11. | Repo angelegt |
| **S4** | Diagramme und Folien | ab Di 17.11., parallel | – |
| **S2** | Keyword-Schichten, Tests, Demo-Szenarien | Mi 18.11. | S1 |
| **S3** | Robocop, README, Jenkins minimal | Do 19.11. | S2 |
| **S5** | Spickzettel und Drehbuch | Fr 20.11. | S2 |
| S6 (optional) | KI-Joker als Screencast | nur bei Zeit | S1 |

Parallel arbeiten: zweite Session in einem eigenen Worktree
(`git worktree add ../rf-device-lab-folien -b folien`).

## Was nicht ins öffentliche Repo gehört

Folien in der imbus-Vorlage, Basisschulung und Drehbuch liegen im separaten Ordner
`workshop-material/` außerhalb des Repos.

## Definition of Done

- Akzeptanzkriterien der Session erfüllt
- `just test` grün, Robocop ohne Fehler (außer in `antipatterns/`)
- Kein `Sleep`, keine Kundenbegriffe, keine Geheimnisse
- `plan/HANDOFF.md` ergänzt
