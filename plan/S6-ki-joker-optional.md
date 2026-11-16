# S6 (optional) – KI-Joker als Screencast

**Nur starten, wenn S1–S5 fertig sind und Zeit bleibt.** Ergebnis ist ein aufgezeichneter
Screencast, keine Live-Demo. Alles lokal, nur mit den erfundenen Daten des Mocks.

## Umfang

Eine Demo mit **robotframework-aiagent** und einem lokalen Vision-Modell über Ollama:

1. `ai/display_check.robot`: Screenshot der Statusseite per Browser Library,
   `Chat` mit Bild und typisiertem Ergebnis (`DisplayReading`: Wert, Einheit),
   Vergleich mit dem REST-Messwert innerhalb einer Toleranz.
2. Klären, wie aiagent ein lokales Ollama-Modell anspricht; Lösung und Modellwahl in
   `ai/README.md`, dazu Chancen und Grenzen in je drei Punkten.
3. Lauf aufzeichnen; Log in `ai/beispiel-log/` ablegen.

## Akzeptanzkriterien

- [ ] Demo läuft lokal ohne Internet
- [ ] Keine API-Schlüssel im Repo
