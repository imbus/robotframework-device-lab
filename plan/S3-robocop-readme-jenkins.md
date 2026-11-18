# S3 – Robocop, README und Jenkins (minimal)

**Ziel:** Genug Qualität und CI, um Block 9 zu zeigen: eine Robocop-Razzia, ein README mit
Schnellstart und eine Jenkins-Pipeline für Screenshot und Screencast.

Voraussetzung: S2 ist fertig.

## Umfang

1. **Robocop** mit Standardregeln; `just lint` und `just format`.
   Hauptcode ohne Befunde, `antipatterns/` mit sichtbaren Befunden.
2. **README.md:** ein Satz, was das ist; **Start in drei Befehlen**; Ordnerübersicht;
   die vier Schichtregeln; Link auf `docs/keywords/`.
3. **`just docs`:** LibDoc für die Library und die Resources nach `docs/keywords/`.
4. **Jenkins lokal**, so einfach wie möglich:
   - `docker-compose.yml` mit Jenkins (LTS, eigenes kleines Image mit Python 3.14 und uv)
     und dem Mock im selben Netz (dafür ein schlankes Dockerfile für `devicehub`)
   - `Jenkinsfile`: `Lint` (Robocop) → `Unit` (pytest) → `Robot` (Profil `ci`, ohne Tag `ui`)
     → Ergebnisse archivieren und mit dem Robot-Framework-Plugin anzeigen
   - Einrichtung des Jobs darf einmalig von Hand passieren; die Schritte stehen in
     `jenkins/EINRICHTUNG.md` (max. 10 Schritte)
   - Quelle: lokales Repo als Volume, damit es offline läuft
   - `just jenkins`, `just jenkins-stop`
5. **`just offline-prepare`:** Images ziehen, Python-Pakete und Playwright-Browser
   vorladen, damit am Workshop-Tag nichts aus dem Netz nötig ist.

## Nicht bauen

Configuration as Code, pre-commit, Devcontainer, ADRs, eigene Robocop-Regeln.

## Akzeptanzkriterien

- [ ] `just lint` zeigt Befunde nur in `antipatterns/`
- [ ] README-Schnellstart funktioniert in einem frischen Klon
- [ ] Jenkins-Lauf grün, Robot-Ergebnisse im Job sichtbar
- [ ] Jenkins-Lauf funktioniert bei ausgeschaltetem WLAN (nach `offline-prepare`)
