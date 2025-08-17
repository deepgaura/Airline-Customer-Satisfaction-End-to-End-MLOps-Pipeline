// Jenkinsfile

def dockerImage

pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        DOCKERHUB_CREDENTIAL_ID = 'mlops-dockerhub'
        DOCKERHUB_REGISTRY = 'https://registry.hub.docker.com'
        DOCKERHUB_REPOSITORY = 'deep2107/prediction-mlops-app'
    }
    
    stages {
        stage('Clonning from Github Repo') {
            steps {
                script {
                    echo 'Clonning from Github Repo...'
                    git branch: 'main',
                        credentialsId: 'mlops-github-token',
                        url: 'https://github.com/deepgaura/MLOPS-PROJECT.git'
                }
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                script {
                    echo 'Setup Virtual Environment...'
                    sh '''
                       python -m venv ${VENV_DIR}
                       . ${VENV_DIR}/bin/activate
                       pip install --upgrade pip 
                       pip install -e .
                    '''
                }
            }
        }

        stage('Linting code') {
            steps {
                script {
                    echo 'Linting code...'
                    sh '''
                     set -e 
                     . ${VENV_DIR}/bin/activate
                     pylint application.py main.py --output=pylint-report.txt --exit-zero || echo "Pylint stage completed"
                     flake8 application.py main.py --ignore=E501,E302 --output-file=flake8-report.txt || echo "Flake8 stage completed"
                     black application.py main.py  || echo "Black stage completed"
                    '''
                }
            }
        }

        stage('Trivy Scanning') {
            steps {
                script {
                    echo 'Trivy Scanning...'
                    sh "trivy fs ./ --format table -o trivy-fs-report.html"
                }
            }
        }

        stage('Building Docker image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    dockerImage = docker.build("${DOCKERHUB_REPOSITORY}:latest")
                }
            }
        }

        stage('Scanning Docker image') {
            steps {
                script {
                    echo 'Scanning Docker image...'
                    sh "trivy image ${DOCKERHUB_REPOSITORY}:latest --format table -o trivy-image-scan-report.html"
                }
            }
        }

        stage('Pushing Docker Image') {
            steps {
                script {
                    echo 'Pushing Docker Image........'
                    docker.withRegistry("${DOCKERHUB_REGISTRY}", "${DOCKERHUB_CREDENTIAL_ID}") {
                        dockerImage.push('latest')
                    }
                }
            }
        }
    }
}
