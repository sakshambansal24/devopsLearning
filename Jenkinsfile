pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv .venv'
                sh '.venv/bin/pip install -r requirements-dev.txt'
            }
        }

        stage('Lint') {
            steps {
                sh '.venv/bin/ruff check .'
            }
        }

        stage('Test') {
            steps {
                sh '.venv/bin/pytest'
            }
        }
    }
}
