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
