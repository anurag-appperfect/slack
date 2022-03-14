pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                cleanWs()
                checkout scm
                bat '''
                    ls
                    docker build -t setup-jitx .
                    docker rm --force test-jitx
                    docker run -dit -v "C:\\Users\lenovo\.jenkins\workspace\slack-test":/myvol1 --name test-jitx setup-jitx
                    docker exec --workdir /myvol1 test-jitx chmod +x jitx.sh
                    # docker exec --workdir /myvol1 test-jitx ./jitx.sh ./ 
                    docker exec --workdir /myvol1 test-jitx ./jitx.sh ./ JITX-QA
                '''
                slackUploadFile filePath: "JITX-QA\\*.html", initialComment:  "HEY HEY"
            }
        }
    }
}

