// Dieselben Werkzeuge wie auf dem Laptop: uv, Robocop, pytest, RobotCode. Start: just jenkins
pipeline {
    agent any
    stages {
        stage('Lint') {
            // Das Anti-Pattern hat absichtlich Befunde
            steps { sh 'uv run robocop check --exclude tests/04_antipatterns' }
        }
        stage('Unit') {
            steps { sh 'uv run pytest' }
        }
        stage('Robot') {
            steps { sh 'uv run robotcode --profile ci robot' }
            // Robot-Framework-Plugin: speichert Log und Report am Build und zeigt die Ergebnisse
            post { always { robot outputPath: 'results' } }
        }
    }
}
