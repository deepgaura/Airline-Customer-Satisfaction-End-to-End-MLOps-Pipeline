def dockerImage

pipeline {
  agent any

  environment {
    VENV_DIR = 'venv'
    DOCKERHUB_CREDENTIAL_ID = 'mlops-dockerhub'
    DOCKERHUB_REGISTRY = 'https://index.docker.io/v1/'
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
        sh """
          python -m venv ${VENV_DIR}
          . ${VENV_DIR}/bin/activate
          pip install --upgrade pip
          pip install -r requirements-dev.txt
          pip install -e .
        """
      }
    }

    stage('Linting code') {
      steps {
        sh """
          set -e
          . ${VENV_DIR}/bin/activate
          pylint application.py main.py --output=pylint-report.txt --exit-zero || true
          flake8 application.py main.py --ignore=E501,E302 --output-file=flake8-report.txt || true
          black application.py main.py || true
        """
      }
    }

    stage('Trivy Scanning (FS)') {
      steps {
        sh '''
          # Skip large/irrelevant dirs for speed
          trivy fs ./ \
            --scanners vuln \
            --skip-dirs venv \
            --skip-dirs .git \
            --skip-dirs __pycache__ \
            --skip-files artifacts/raw/data.csv \
            --format table -o trivy-fs-report.html || true
        '''
      }
    }

    stage('Building Docker image') {
      steps {
        script {
          echo 'Building Docker image...'
          sh 'docker pull docker.io/library/python:3.11-slim || true' // pre-pull base
          retry(2) {
            dockerImage = docker.build("${DOCKERHUB_REPOSITORY}:latest", ".")
          }
        }
      }
    }

    stage('Scanning Docker image') {
      steps {
        sh "trivy image ${DOCKERHUB_REPOSITORY}:latest --format table -o trivy-image-scan-report.html || true"
      }
    }

    stage('Pushing Docker Image') {
      steps {
        script {
          echo 'Pushing Docker Image...'
          docker.withRegistry("${DOCKERHUB_REGISTRY}", "${DOCKERHUB_CREDENTIAL_ID}") {
            dockerImage.push('latest')
            dockerImage.push("build-${BUILD_NUMBER}")
          }
        }
      }
    }
  }
}
