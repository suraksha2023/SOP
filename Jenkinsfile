pipeline {
    agent any

    environment {
        // Python command (assuming python3 is installed)
        PYTHON = "python3"
    }

    stages {

        stage('Clean Workspace') {
            steps {
                // Skip cleaning to avoid locked files
                echo "Skipping workspace cleanup to avoid locked files"
            }
        }

        stage('Checkout Code') {
            steps {
                git(
                    url: 'https://github.com/suraksha2023/SOP.git',
                    branch: 'master',
                    credentialsId: ''   // Add if private
                )
            }
        }

        stage('Setup Python Environment') {
            steps {
                // Create virtual environment
                sh "${env.PYTHON} -m venv venv"

                // Upgrade pip
                sh "venv/bin/python -m pip install --upgrade pip"

                // Install dependencies
                sh "venv/bin/python -m pip install -r requirements.txt"
            }
        }

        stage('Run Tests') {
            steps {
                // Run pytest
                sh "venv/bin/python -m pytest -v tests"
            }
        }

        stage('Publish Reports') {
            steps {
                publishHTML([
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'report.html',
                    reportName: 'Pytest HTML Report'
                ])
            }
        }
    }

    post {
        always {
            echo "Build finished — cleanup done."
        }
        success {
            echo "Build succeeded!"
        }
        failure {
            echo "Build failed!"
        }
    }
}
