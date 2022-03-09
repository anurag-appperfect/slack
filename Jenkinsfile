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
                echo "Hello world" > output.txt
                git add .
                git commit -m "Added file with"
                git remote add origin https://github.com/anurag-appperfect/slack.git
                git branch -M main
                git push -u origin main
                '''
            }
        }
    }
}
