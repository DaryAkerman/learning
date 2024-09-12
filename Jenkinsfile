pipeline{
    
    agent{
        kubernetes{
            label 'learning'
            idleMinutes 5
            yamlFile 'build-jenkins-agent.yaml'
            defaultContainer 'ez-docker-helm-build'
        }
    }

    environment{
        DOCKER_IMAGE = 'winterzone2/learningjenkins'
        GITHUB_REPO = 'DaryAkerman/learning'
        GITHUB_TOKEN = credentials('github-creds')
        VERSION = "1.0.${BUILD_NUMBER}"
    }

    stages{
        stage("Checkout"){
            steps{
                checkout scm
            }
        }
 
        stage("Build Docker Image"){
            steps{
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:latest", "--no-cache .")
                }
            }
        }

        stage("Push Docker Image"){
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-creds') {
                        dockerImage.push("${VERSION}")
                        dockerImage.push("latest")
                    }
                }
            }
        }

    }
}