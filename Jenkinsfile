pipeline {
    agent any

    environment{
        VENV_DIR = 'venv'
    }
    
    stages {
        stage('Cloning from Github Repo') { 
            steps {
                script { 
                    // Cloning github repo
                    echo 'Cloning from Github Repo...' 
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'mlops-github-token', url: 'https://github.com/Vedant1124/MLOPS-PROJECT.git']])
                }
            }
        }

        stage('Setup Virtual Environment') { 
            steps {
                script { 
                    // Setup Virtual Environment
                    echo 'Setup Virtual Environment...' 
                    sh '''
                        python-m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -e .
                    '''
                }
            }
        }

        stage('Linting Code') { 
            steps {
                script { 
                    // Linting Code
                    echo 'Linting Code...' 
                }
            }
        }
    }
}