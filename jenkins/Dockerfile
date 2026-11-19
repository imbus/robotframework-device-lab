# Jenkins mit uv, Python 3.14, allen Paketen aus uv.lock und Chromium für den Web-UI-Test.
# Alles liegt im Image, die Pipeline lädt nichts nach.
FROM jenkins/jenkins:2.580.2-lts-jdk21
COPY --from=ghcr.io/astral-sh/uv:0.13.8 /uv /usr/local/bin/uv
RUN jenkins-plugin-cli --plugins workflow-aggregator git robot

USER root
# Das eingehängte Repo gehört einem anderen Benutzer; Git soll es trotzdem lesen dürfen.
RUN git config --system --add safe.directory '*'

# Eine Python-Umgebung für alle Builds. Node.js steckt in robotframework-browser-batteries
# (braucht libatomic1); --with-deps installiert die Systembibliotheken für Chromium.
ENV UV_PYTHON_INSTALL_DIR=/opt/python UV_PROJECT_ENVIRONMENT=/opt/venv
COPY pyproject.toml uv.lock /opt/project/
RUN apt-get update && apt-get install -y --no-install-recommends libatomic1 \
    && cd /opt/project && uv sync --frozen --no-cache \
    && uv run --no-sync rfbrowser install --with-deps chromium \
    && rm -rf /var/lib/apt/lists/* \
    && chown -R jenkins:jenkins /opt/python /opt/venv
USER jenkins
