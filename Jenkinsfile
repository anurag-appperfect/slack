pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                bat '''
                cd Exporter-QA
                pytest test_exporter_jitx.py
                '''
            }
        }
    }
}
