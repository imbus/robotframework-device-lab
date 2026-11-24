# KI-Joker: Statusseite mit lokalem Vision-Modell ablesen

Ein Vision-Modell liest den Messwert auf der Statusseite ab, wie ein Mensch es tun würde. Das
Ergebnis ist typisiert (`DisplayReading`: Wert und Einheit). Python prüft es gegen den Messwert,
den das Gerät über REST liefert (Toleranz 1 %). Alles läuft lokal, ohne Internet und ohne
API-Schlüssel.

Ablauf in [`display_check.robot`](display_check.robot): Gerät mit 12 V betreiben → Statusseite
öffnen → Bildschirmfoto → `Chat` mit Bild → `DisplayReading(value=12.008, unit='V')` → Vergleich
mit REST. Ein Beispiel-Log liegt in [`beispiel-log/log.html`](beispiel-log/log.html).

## Einrichten (einmalig, mit Internet)

```bash
brew install ollama
ollama serve                 # eigenes Terminal (oder dauerhaft: brew services start ollama)
ollama pull qwen3-vl:8b      # Vision-Modell, ca. 6 GB
uv sync --group ai           # robotframework-aiagent; just ki holt die Gruppe sonst selbst
```

## Starten (ohne Internet)

```bash
just sim                     # Terminal 1: Mock-Gerät
ollama serve                 # Terminal 2, falls nicht als Dienst gestartet
just ki                      # Terminal 3
```

`just test` lässt den KI-Joker aus (Tag `ki`). Damit brauchen Workshop-Rechner und Jenkins kein Ollama.

## So spricht robotframework-aiagent ein lokales Ollama-Modell an

- **Modellname** `ollama:qwen3-vl:8b`: aiagent gibt ihn an pydantic-ai weiter. Dessen
  Ollama-Anbieter nutzt die OpenAI-kompatible Schnittstelle von Ollama.
- **Adresse:** `OLLAMA_BASE_URL=http://127.0.0.1:11434/v1`. Das Profil `ki` in `robot.toml` setzt
  sie unter `env`.
- **Kein Schlüssel:** Ohne `OLLAMA_API_KEY` setzt pydantic-ai selbst einen Platzhalter ein.
- **Paket:** `robotframework-aiagent-slim[openai]` statt des Metapakets mit allen Anbietern. Es
  enthält nur den OpenAI-kompatiblen Client.
- **Bild:** Die Library `AIAgent.Content` lädt das Bildschirmfoto mit `Load Binary Content`. Es
  geht als weiteres Argument an `Chat`. (Das Doku-Beispiel mit `attachments=` gibt es in 0.4 nicht.)
- **Typisiertes Ergebnis:** `output_type=${{display_reading.DisplayReading}}` direkt am `Chat`
  gibt die Dataclass aus [`display_reading.py`](display_reading.py) an. `Chat` liefert dann
  sofort ein `DisplayReading`-Objekt.

## Modellwahl

`qwen3-vl:8b` kann Bilder lesen und typisierte Ergebnisse liefern. Es passt mit rund 6 GB
bequem in den Speicher. Gemessen auf einem M3 Pro mit 36 GB:

| Zeitpunkt | Dauer von `Chat` |
| --- | --- |
| erster Aufruf (Modell wird geladen) | ca. 20 s |
| danach | ca. 14 s |

Ein großer Teil der Zeit ist „Thinking“. Im Log lässt es sich aufklappen und zeigt, wie das Modell
abliest. Ohne Thinking (`model_settings={'thinking': False}`) braucht ein Aufruf ca. 11 s, bei
gleichem Ergebnis. Für die Demo bleibt es trotzdem an, weil die sichtbare Begründung dort zählt.
Ein anderes Modell wählt man mit `just ki --variable KI_MODELL:ollama:<name>`. Getestet ist nur
`qwen3-vl:8b`.

## Chancen

1. **Prüft, was ein Mensch sieht:** Anzeigen ohne `data-testid` oder API lassen sich prüfen,
   später auch ein Gerätedisplay per Kamerabild.
2. **Typisiert statt geparst:** kein Regex auf Freitext. Die Prüfung bleibt deterministisch in
   Python.
3. **Lokal:** Keine Daten verlassen den Rechner, es gibt keine Kosten pro Aufruf und keinen
   Schlüssel zu verwalten.

## Grenzen

1. **Langsam:** Eine Ablesung dauert ca. 15 s, REST oder ein Selektor nur Millisekunden. Für viele
   Messpunkte taugt das nicht.
2. **Nicht deterministisch:** Das Modell kann sich verlesen, und das Ergebnis hängt von Modell und
   Version ab. Deshalb nie allein entscheiden lassen, sondern immer gegen eine zweite Quelle prüfen
   (hier REST).
3. **Aufwand:** 6 GB Modell und viel Arbeitsspeicher. aiagent ist noch in Version 0.x, Schnittstellen
   können sich ändern.
