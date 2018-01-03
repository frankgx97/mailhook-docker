pipeline {
  agent any
  stages {
    stage('Preparation') {
      steps {
        git(url: 'https://github.com/nyanim/mailhook.git', branch: 'master', credentialsId: '9ad60ea9-8650-4bb2-8d59-6fd9500d48a2')
      }
    }
    stage('Build') {
      steps {
        sh 'sudo docker build --force-rm -t nyanim/mailhook:latest .'
      }
    }
    stage('Deploy') {
      parallel {
        stage('Deploy') {
          steps {
            sh '''
            sudo docker login -u=$DOCKER_USERNAME -p=$DOCKER_PASSWORD
            sudo docker push nyanim/mailhook:latest
            '''
            sh '''
            sshpass -p $SSH_PASSWORD ssh -o StrictHostKeyChecking=no -l $SSH_USER $SSH_QCL_HOST <<EOF 
            echo $SSH_PASSWORD | sudo -S docker-compose -f $MAILHOOK_COMPOSE_FILE down
            sudo docker pull nyanim/mailhook:latest
            sudo docker-compose -f $MAILHOOK_COMPOSE_FILE up -d 
            uname -a
            '''
          }
        }
        stage('Cleanup') {
          steps {
            sh '''
            sudo docker images | grep \'<none>\' | awk \'{print $3}\' | xargs sudo docker rmi || true
            '''
          }
        }
      }
    }
    stage('Notification') {
      steps {
        emailext(body: '''$PROJECT_NAME - Build # $BUILD_NUMBER - $BUILD_STATUS:
Check console output at $BUILD_URL to view the results.''', recipientProviders: [[$class: 'DevelopersRecipientProvider']], replyTo: '$MAIL', subject: '$PROJECT_NAME - Build # $BUILD_NUMBER - $BUILD_STATUS!', to: '$MAIL')
      }
    }
  }
}