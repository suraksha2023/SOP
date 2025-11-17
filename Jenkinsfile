pipeline {
    agent any

    environment {
        // Path to Python executable if not in system PATH
        PYTHON = "python"
    }

    stages {

        stage('Clean Workspace') {
            steps {
                // Remove everything in workspace including old .git and venv
                //deleteDir()
                echo "Skipping workspace cleanup to avoid locked files"
            }
        }

        stage('Checkout Code') {
            steps {
                git(
                    url: 'https://github.com/DruvakumarJS/py_uconnect.git',
                    branch: 'master', // Use exact branch from your repo
                    credentialsId: ''  // Fill in if your repo is private
                )
            }
        }

        stage('Setup Python Environment') {
            steps {
                // Create a virtual environment
                bat "${env.PYTHON} -m venv venv"

                // Upgrade pip inside the venv
                bat "venv\\Scripts\\python.exe -m pip install --upgrade pip"

                // Install dependencies from requirements.txt (including xlrd==1.2.0)
                bat "venv\\Scripts\\python.exe -m pip install -r requirements.txt"
            }
        }

        stage('Run Tests') {
            steps {
                // Run pytest on the tests folder (ensure lowercase 'tests/')
                bat "venv\\Scripts\\python.exe -m pytest -v tests"

                // Add workspace to PYTHONPATH for imports
              // bat 'set PYTHONPATH=%CD% && venv\\Scripts\\python.exe -m pytest -v tests'

            //   bat '.\\run_tests.bat'
            }
        }

        stage('Publish Reports') {
            steps {
                // Example: archive pytest XML reports if generated
                //junit '**/test-reports/*.xml'
               // junit 'reports/results.xml'
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
            echo "Build finished — workspace cleaned up if needed."
        }
        success {
            echo "Build succeeded!"
        }
        failure {
            echo "Build failed!"
        }
    }
}
