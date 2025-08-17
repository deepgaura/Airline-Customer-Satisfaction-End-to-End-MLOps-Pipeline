pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }
    
    stages {
        stage('Clonning from Github Repo') {
            steps {
                script {
                    echo 'Clonning from Github Repo...'
                    checkout scmGit(
                        branches: [[name: '*/main']],
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'mlops-github-token',
                            url: 'https://github.com/deepgaura/MLOPS-PROJECT.git'
                        ]]
                    )
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
                    // 👇 Disable BuildKit so proxy is respected
                    sh 'DOCKER_BUILDKIT=0 docker build -t mlops .'
                }
            }
        }

        stage('Scanning Docker image') {
            steps {
                script {
                    echo 'Scanning Docker image...'
                    sh "trivy image mlops:latest --format table -o trivy-image-scan-report.html"
                }
            }
        }
    }
}
