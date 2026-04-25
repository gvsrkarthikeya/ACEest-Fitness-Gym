pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "gvsrkarthikeya/aceest-fitness-gym"
        DOCKER_HUB   = credentials('dockerhub-creds')
    }

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
                sh '''
                docker build -t ${DOCKER_IMAGE}:latest .
                '''
            }
        }

        stage('Login to Docker Hub') {
            steps {
                sh '''
                echo "${DOCKER_HUB_PSW}" | docker login \
                -u "${DOCKER_HUB_USR}" --password-stdin
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                sh '''
                docker push ${DOCKER_IMAGE}:latest
                '''
            }
        }
    }

    post {
        success {
            echo 'Docker image built and pushed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check logs.'
        }
    }
}

