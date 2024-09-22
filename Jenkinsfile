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
                        // Use sed to directly update the version tag in values.yaml
                        sh """
                        # Ensure you are on the correct branch
                        git config --global --add safe.directory $WORKSPACE
                        git checkout main
                        
                        # Update the tag using sed
                        sed -i 's/tag: ".*"/tag: "${VERSION}"/' chart/values.yaml
                        
                        # Verify the updated values.yaml
                        cat chart/values.yaml

                        # Configure Git
                        git config user.email "daryakerman200@gmail.com"
                        git config user.name "Jenkins CI"
                        git pull origin main
                        
                        # Add and commit the changes
                        git add chart/values.yaml
                        git update-index --refresh

                        # Check for staged changes
                        if git diff --cached --name-only | grep -q 'chart/values.yaml'; then
                            echo "Changes detected, committing..."
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
