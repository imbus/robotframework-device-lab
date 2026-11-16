# S1 – Mock-Gerät, Library, Testdaten, robot.toml

**Ziel:** Die technische Grundlage aller Demos: ein simuliertes Messgerät hinter einer
REST-API, die Python-Library, die es anspricht, und Testdaten für zwei Gerätevarianten.

## Umfang

1. **Gerüst:** `pyproject.toml` mit uv, Ordner laut CLAUDE.md, `.gitignore`, `LICENSE` (MIT),
   `justfile` mit `sim`, `test`, `test-a`, `test-b`, `dryrun`.
2. **Mock `devicehub/`** (FastAPI, Start mit `just sim` auf Port 8080):
   - Zwei Geräte: `mm100-a` und `mm100-b` mit Seriennummer und Firmware-Version;
     Variante B hat andere Registeradressen (z. B. 41001/31001/31002/31010)
   - Zustände `OFF → BOOTING → SETTLING → READY → MEASURING → READY`, dazu `FAULT`;
     Dauer realistisch (20 s / 30 s) × `SIM_TIME_SCALE` (Standard 0.1)
   - Messwert = Sollwert + reproduzierbares Rauschen (`SIM_SEED`)
   - Endpunkte: `/health`, `/devices`, `/devices/{id}`, `/devices/{id}/power`,
     `/devices/{id}/state`, `/devices/{id}/registers/{address}` (GET/PUT),
     `/devices/{id}/measurements` (starten, Ergebnis abholen), `/devices/{id}/reset`
   - Fehler-Injektion `POST /sim/faults` mit `hang` (bleibt in SETTLING), `drift`
     (Messwert läuft weg), `disconnect` (503); `DELETE /sim/faults`
   - Eine Web-Seite `/ui/devices/{id}`: Zustand, Messwert, Buttons Ein/Aus, alles mit `data-testid`
3. **`libraries/DeviceHubLibrary/`** (englische Keyword-Namen):
   - Dataclasses `DeviceProfile`, `MeasurementPoint`, `Expectation`, `Reading`
   - `Load Device Profile` (JSON → Dataclasses, klare Fehlermeldung bei falschen Feldern)
   - `Connect To DeviceHub`, `Power On Device`, `Power Off Device`
   - `Wait Until Device State Is    state    timeout` (Polling, kein Sleep)
   - `Write Register`, `Read Register` (Adresse aus dem Profil)
   - `Run Measurement Group` → Liste von `Reading`
   - `Readings Should Match Expectation` → **HTML-Tabelle im Log**, lesbare Fehlermeldung
   - `Reset Device To Safe State`, `Get Device Metadata`
   - Docstrings auf Deutsch
4. **Testdaten:** `testdata/devices/variante_a.json`, `variante_b.json` (je 3 Messpunkte,
   Format laut CLAUDE.md).
5. **`robot.toml`** mit Profilen: Standard (Variante A, `results/`), `variante-a`, `variante-b`,
   `ci`; `.robot.toml` in `.gitignore`.
6. **Zwei pytest-Tests** für die Library (Profil laden, Toleranzprüfung), damit die
   Pipeline später eine Unit-Stufe zeigen kann.
7. Ein Smoke-Test `tests/01_smoke/geraet_erreichbar.robot` (Firmware lesen).

## Nicht bauen

Docker für den Mock, JSON-Schema, weitere UI-Seiten, umfangreiche Unit-Tests.

## Akzeptanzkriterien

- [ ] `just sim` startet den Mock, `/docs` zeigt die API
- [ ] Gerät einschalten → nach ca. 5 s `READY` (bei `SIM_TIME_SCALE=0.1`)
- [ ] Jede der drei Fehlerarten ist ein- und ausschaltbar und im Verhalten erkennbar
- [ ] Smoke-Test grün mit `just test-a` und `just test-b`
- [ ] `Readings Should Match Expectation` zeigt im Log eine gut lesbare Tabelle
- [ ] Ein fehlerhaftes JSON scheitert mit verständlicher Meldung
- [ ] `uv run pytest` grün
