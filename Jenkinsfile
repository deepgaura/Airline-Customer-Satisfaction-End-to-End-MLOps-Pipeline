pipeline {
    agent any
    
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
    }
}