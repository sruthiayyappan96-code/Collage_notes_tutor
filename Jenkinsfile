pipeline {
    agent any

    environment {
        IMAGE = 'studymate-rag-assistant'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE%:latest .'
            }
        }

        stage('Test') {
            steps {
                bat 'docker run --rm %IMAGE%:latest python -m py_compile app.py'
            }
        }
    }

    post {
        success { echo 'Pipeline finished successfully' }
        failure { echo 'Pipeline failed. Check the console output' }
    }
}