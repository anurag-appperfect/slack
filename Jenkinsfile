pipeline {
    agent any
    stages {
        stage ('Tests on Ubuntu bionic') {
            steps {
                cleanWs()
                checkout scm
                sh 'pwd'
                slackUploadFile filePath: "*.txt", initialComment:  "HEY HEY"
            }
        }
    }
}
