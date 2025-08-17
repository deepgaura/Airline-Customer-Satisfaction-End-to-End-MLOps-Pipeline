pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }
    
    stages {
        stage('Clonning from Github Repo') {
            steps {
                script {
                    // Cloning Github Repo
                    echo 'Clonning from Github Repo...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'mlops-github-token', url: 'https://github.com/deepgaura/MLOPS-PROJECT.git']])
                }
            }
        }

         stage('Setup Virtual Environment') {
            steps {
                script {
                    // Setup Virtual Environment
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
                    // Linting code
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
                    // Trivy Scanning
                    echo 'Trivy Scanning...'
                    sh "trivy fs ./ --format table -o trivy-fs-report.html"
                }
            }
        }
       stage('Building Docker image') {
    steps {
        script {
            echo 'Building Docker image...'
            sh '''
                docker build -t mlops \
                  --build-arg HTTP_PROXY=http://http.docker.internal:3128 \
                  --build-arg HTTPS_PROXY=http://http.docker.internal:3128 \
                  --build-arg NO_PROXY=localhost,127.0.0.1,hubproxy.docker.internal,.docker.internal .
            '''
        }
    }
}
        stage('Scanning Docker image') {
            steps {
                script {
                    // Scanning Docker image
                    echo 'Scanning Docker image...'
                    sh "trivy image mlops:latest --format table -o trivy-image-scan-report.html"
                }
            }
        }

    }
}