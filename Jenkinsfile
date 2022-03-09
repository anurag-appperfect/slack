pipeline {
    agent any
    options {
        skipDefaultCheckout(true)
    }
    stages {
        stage('build') {
            steps {
                cleanWs()
                checkout scm
                bat '''
                cd Exporter-QA
                echo "Hello world" > output.txt
                git add .
                git commit -m "Added file with"
                git push origin main
                '''
            }
        }
    }
}
