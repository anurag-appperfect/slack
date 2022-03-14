pipeline {
    agent none
    options {
        skipDefaultCheckout(true)
    }
    stages {
        stage ('Running tests on several platforms'){
            parallel {
                stage ('Tests on Ubuntu bionic') {
                    steps {
                        cleanWs()
                        checkout scm
                        sh 'pwd'
                        sh '''
                             ls
                             docker build -t setup-jitx .
                             docker run -dit -v $(pwd):/myvol3 --name test-jitx setup-jitx
                             docker exec --workdir /myvol3 test-jitx chmod +x jitx.sh
                             # docker exec --workdir /myvol3 test-jitx ./jitx.sh ./ 
                             docker exec --workdir /myvol3 test-jitx ./jitx.sh ./ Exporter-QA
                             docker exec --workdir /myvol3 test-jitx python merge_report.py
                        '''
                        slackUploadFile filePath: "\Exporter-QA\*.html", initialComment:  "HEY HEY"
                    }
                }
            }
        }
    }
}
