pipeline {
    agent any
    environment {
        EMAIL_RECIPIENT = 'qasimalik@gmail.com'
    }
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/effendii69/todo-list-tests.git'
            }
        }
        stage('Test') {
            steps {
                script {
                    docker.image('python:3.9-slim').inside('--user root') {
                        sh 'apt-get update && apt-get install -y chromium-driver chromium'
                        sh 'pip install -r requirements.txt'
                        sh 'python3 -m pytest test_todo_app.py --junitxml=test-results.xml --headless'
                    }
                }
            }
        }
    }
    post {
        always {
            node {
                junit 'test-results.xml'
                emailext (
                    subject: "Test Results for ${env.JOB_NAME} [${env.BUILD_NUMBER}]",
                    body: "Please find the test results attached.",
                    to: "${EMAIL_RECIPIENT}",
                    attachmentsPattern: 'test-results.xml'
                )
            }
        }
    }
}
