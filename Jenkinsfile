pipeline {
    agent any
    stages {
        stage('Install dependencies') {
            steps {
                sh 'python3 -m pip install -r requirements.txt'
            }
        }
        stage('Lint') {
            steps {
                sh 'python3 -m pip install flake8 && python3 -m flake8 app.py program_data.py'
            }
        }
        stage('Test') {
            steps {
                sh 'python3 -m pytest'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t aceest-fitness-gym:latest .'
            }
        }
    }
}
