pipeline {
    agent any

    environment{
        VENV_DIR = "venv"
    }
    
    stages {
        stage('Cloning from Github Repo...') {
            steps {
                script {
                    echo 'Cloning from Github Repo......'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'Airline-github-token', url: 'https://github.com/Vedant1124/MLOPS-PROJECT.git']])
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

        stage('Linting Code') { 
            steps {
                script { 
                    // Linting Code
                    echo 'Linting Code...' 
                    sh '''
                        set -e
                        . ${VENV_DIR}/bin/activate

                        pylint application.py main.py --output=pylint-report.txt --exit-zero || echo "Pylint stage completed"
                        flake8 application.py main.py --ignore=E501 ,E302 --output-file=flake8-report.txt || echo "Flake 8 stage completed"
                        black application.py main.py || echo "Black stage completed"
                    '''
                }
            }
        }
    }
}