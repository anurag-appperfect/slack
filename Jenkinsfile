pipeline {
    agent any
    stages {
        stage ('Tests on Ubuntu bionic') {
            steps {
                cleanWs()
                checkout scm
                sh 'pwd'
                sh '''
                   ls
                   docker build -t setup-jitx .
                   docker run -dit --name test-jitx setup-jitx
                   docker exec test-jitx chmod +x jitx.sh
                   # docker exec test-jitx ./jitx.sh ./ 
                   docker exec test-jitx ./jitx.sh ./ Exporter-QA
                   docker exec test-jitx python merge_report.py
                '''
            }
        }
    }
}
