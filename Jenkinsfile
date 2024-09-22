pipeline {
    agent {
        kubernetes {
            label 'learning'
            idleMinutes 5
            yamlFile 'build-jenkins-agent.yaml'
            defaultContainer 'ez-docker-helm-build'
        }
    }

    environment {
        DOCKER_IMAGE = 'winterzone2/learningjenkins'
        GITHUB_REPO = 'DaryAkerman/learning'
        GITHUB_TOKEN = credentials('github-creds')
        VERSION = "1.0.${BUILD_NUMBER}"
    }

    stages {
        stage("Checkout") {
            steps {
                checkout scm
            }
        }

        stage("Build Docker Image") {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:latest", "--no-cache .")
                }
            }
        }

        stage("Update values.yaml") {
            steps {
                script {
                    // Use sed to replace the tag in values.yaml with the current version
                    sh "sed -i 's/tag: \"latest\"/tag: \"${VERSION}\"/' chart/values.yaml"
                }
            }
        }

        stage("Push Docker Image") {
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

        stage("Push changes to GitHub") {
            steps {
                script {
                    // Commit the updated values.yaml with the new version
                    sh """
                    git config user.email "daryakerman200@gmail.com"
                    git config user.name "DaryAkerman"
                    git add chart/values.yaml
                    git commit -m "Update image tag to version ${VERSION}"
                    git push https://${GITHUB_TOKEN}@github.com/${GITHUB_REPO}.git HEAD:main
                    """
                }
            }
        }
    }
}
