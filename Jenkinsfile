pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                sh '''
                cd Exporter-QA
                pytest test_exporter_jitx.py
                '''
            }
        }
    }
}
