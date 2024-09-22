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

                        // Configure Git, force refresh index and commit
                        sh """
                        git config --global --add safe.directory $WORKSPACE
                        git checkout main  # Ensure you're on the main branch
                        git config user.email "daryakerman200@gmail.com"
                        git config user.name "Jenkins CI"
                        git pull origin main
                        
                        # Refresh Git index and ensure detection of changes
                        git update-index --refresh

                        # Check the Git status to ensure the file is tracked and changed
                        git status

                        # Force add the values.yaml file to Git
                        git add chart/values.yaml

                        # Check if the file is staged for commit
                        if git diff --cached --name-only | grep -q 'chart/values.yaml'; then
                            echo "File has changed, committing..."
                            git commit -m "Update image tag to version ${VERSION}"
                            git push https://$GITHUB_USER:$GITHUB_TOKEN_PSW@github.com/${GITHUB_REPO}.git HEAD:main
                        else
                            echo "No changes detected in values.yaml"
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
