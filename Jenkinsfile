pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/gvsrkarthikeya/ACEest-Fitness-Gym.git'
            }
        }
        stage('Check Files') {
            steps {
                sh 'ls -l'
                sh 'ls -l tests/'
                sh 'ls -l tests/test_app.py'
                sh 'test -f tests/test_app.py && echo "File exists" || echo "File missing"'
                sh 'test -d tests && echo "Directory exists" || echo "Directory missing"'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'python3 -m pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'python3 -m pytest'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t aceest-fitness-gym .'
            }
        }
    }
}
