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
                    // Use Groovy's built-in file handling to replace the version tag in values.yaml
                    def valuesFile = readFile 'chart/values.yaml'
                    valuesFile = valuesFile.replace('tag: "latest"', "tag: \"${VERSION}\"")
                    writeFile file: 'chart/values.yaml', text: valuesFile
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
                dir("${WORKSPACE}") {  // Ensure you're in the right directory
                    withCredentials([usernamePassword(credentialsId: 'github-creds', usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN_PSW')]) {
                        script {
                            sh """
                            git config user.email "daryakerman200@gmail.com"
                            git config user.name "Jenkins CI"
                            git add chart/values.yaml
                            git commit -m "Update image tag to version ${VERSION}"
                            git push https://${GITHUB_USER}:${GITHUB_TOKEN_PSW}@github.com/${GITHUB_REPO}.git HEAD:main
                            """
                        }
                    }
                }
            }
        }
    }
}
