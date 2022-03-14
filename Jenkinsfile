pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                cleanWs()
                checkout scm
                sh 'pwd'
                sh '''
                    ls
                    docker build -t setup-jitx .
                    docker rm --force test-jitx
                    docker run -dit -v $(pwd):/myvol3 --name test-jitx setup-jitx
                    docker exec --workdir /myvol3 test-jitx chmod +x jitx.sh
                    # docker exec --workdir /myvol3 test-jitx ./jitx.sh ./ 
                    docker exec --workdir /myvol3 test-jitx ./jitx.sh ./ JITX-QA
                '''
                slackUploadFile filePath: "Exporter-QA\\*.html", initialComment:  "HEY HEY"
            }
        }
    }
}

