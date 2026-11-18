# Befehle für robotframework-device-lab. `just` ohne Argument zeigt die Liste.

# Alle Befehle anzeigen
default:
    @just --list

# Mock-Gerät DeviceHub starten (API-Doku: http://127.0.0.1:8080/docs)
sim:
    uv run uvicorn devicehub.app:app --host 127.0.0.1 --port 8080

# Alle Tests mit dem Standardprofil (Variante A)
test *args:
    uv run robotcode robot {{args}}

# Alle Tests gegen Variante A
test-a *args:
    uv run robotcode --profile variante-a robot {{args}}

# Alle Tests gegen Variante B
test-b *args:
    uv run robotcode --profile variante-b robot {{args}}

# Trockenlauf: prüft Syntax und Keywords, ohne das Gerät anzusprechen
dryrun *args:
    uv run robotcode robot --dryrun {{args}}

# Fehler-Quiz 1, 2 oder 3: die Messung scheitert – warum?
quiz nummer:
    uv run robotcode --profile quiz-{{nummer}} robot

# Absichtlich schlechtes Beispiel ausführen (läuft trotzdem grün)
antipattern:
    uv run robotcode --profile antipattern robot

# Demo zurücksetzen: Mock-Fehler aus, Geräte aus, results/ leer; LÖSCHT neue Profile in data/devices/
reset:
    -curl -sS -X POST http://127.0.0.1:8080/sim/reset
    rm -rf results
    @# Schutz: ohne eingecheckte Profile würde git clean auch variante_a/b löschen
    @git ls-files --error-unmatch data/devices > /dev/null 2>&1 || (echo "Abbruch: data/devices ist nicht eingecheckt" && exit 1)
    git clean -fq data/devices
