pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', 
                url: 'https://github.com/effendii69/todo-list-tests.git'
            }
        }
        stage('Test') {
            agent {
                docker {
                    image 'python:3.9-slim'
                    args '-u root' // Run as root to avoid permission issues
                }
            }
            steps {
                sh '''
                apt-get update && apt-get install -y python3-pip
                pip install -r requirements.txt
                python -m pytest --junitxml=test-results.xml
                '''
            }
        }
    }
    post {
        always {
            junit 'test-results.xml'
            emailext (
                subject: "Test Results - ${currentBuild.currentResult}",
                body: "See ${env.BUILD_URL}",
                to: "qasimalik@gmail.com"
            )
        }
    }
}

