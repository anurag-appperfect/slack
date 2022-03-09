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
                pytest test_exporter_jitx.py --html=report.html
                git status
                '''
            }
        }
    }
}
