pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/gvsrkarthikeya/ACEest-Fitness-Gym.git'
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
