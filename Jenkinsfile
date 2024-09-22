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

        stage("Update and Push values.yaml") {
            steps {
                withCredentials([usernamePassword(credentialsId: 'github-creds', usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN_PSW')]) {
                    script {
                        // Update the values.yaml file
                        def valuesFile = readFile 'chart/values.yaml'
                        valuesFile = valuesFile.replace('tag: "latest"', "tag: \"${VERSION}\"")
                        writeFile file: 'chart/values.yaml', text: valuesFile

                        // Debug step to check the content of values.yaml
                        sh "cat chart/values.yaml"

                        // Configure Git, commit, and push changes to GitHub
                        sh """
                        git config --global --add safe.directory $WORKSPACE
                        git checkout main  # Ensure you're on the main branch
                        git config user.email "daryakerman200@gmail.com"
                        git config user.name "Jenkins CI"
                        git pull origin main
                        git add chart/values.yaml
                        
                        # Only commit if there are changes
                        if git diff-index --quiet HEAD --; then
                            echo "No changes to commit."
                        else
                            git commit -m "Update image tag to version ${VERSION}"
                            git push https://$GITHUB_USER:$GITHUB_TOKEN_PSW@github.com/${GITHUB_REPO}.git HEAD:main
                        fi
                        """
                    }
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
    }
}
