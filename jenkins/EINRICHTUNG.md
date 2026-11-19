# Jenkins lokal einrichten (einmalig)

Jenkins läuft in Docker und baut den **letzten Commit** des lokalen Repos (eingehängt als `/repo`).
Nicht committete Änderungen sieht Jenkins nicht. Der Mock-Container dagegen wird bei jedem
`just jenkins` aus dem aktuellen Ordner gebaut.

1. Docker Desktop (oder Rancher Desktop) starten.
2. `just jenkins`. Der erste Start baut die Images und lädt Python, Pakete und Chromium
   (Internet nötig, je nach Verbindung 5–15 Minuten). Danach startet Jenkins in Sekunden.
3. <http://localhost:8081> öffnen (keine Anmeldung, nur lokal erreichbar).
4. **Element anlegen** (New Item) → Name `device-lab` → **Pipeline** → **OK**.
5. Unter **Pipeline**: Definition **Pipeline script from SCM**, SCM **Git**.
6. Repository URL: `/repo`
7. Branch Specifier: `*/main` (oder der Branch, der gezeigt werden soll).
8. **Speichern** → **Jetzt bauen** (Build Now).
9. Ergebnis: im Build auf **Robot Results**; dort öffnet sich auch `log.html`.

Stoppen mit `just jenkins-stop`. Job und Builds bleiben erhalten.
Ganz von vorn: `docker compose down -v` (löscht das Jenkins-Volume).
