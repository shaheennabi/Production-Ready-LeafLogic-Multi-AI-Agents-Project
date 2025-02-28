pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO = '445567117176.dkr.ecr.us-east-1.amazonaws.com/leaflogic'
        IMAGE_TAG = 'latest'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/shaheennabi/Production-Ready-LeafLogic-Internship-Project', branch: 'main'
            }
        }

        stage('Build and Push to ECR') {
            steps {
                withCredentials([
                    string(credentialsId: 'aws_access_key_id', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws_secret_access_key', variable: 'AWS_SECRET_ACCESS_KEY'),
                    string(credentialsId: 'openai_api_key', variable: 'OPENAI_API_KEY'),
                    string(credentialsId: 'serper_api_key', variable: 'SERPER_API_KEY'),
                    string(credentialsId: 'sender_password', variable: 'SENDER_PASSWORD'),
                    string(credentialsId: 'sender_email', variable: 'SENDER_EMAIL'),
                    string(credentialsId: 'exa_api_key', variable: 'EXA_API_KEY')
                ]) {
                    script {
                        sh """
                        # Configure AWS CLI
                        aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID}
                        aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}
                        aws configure set region ${AWS_REGION}

                        # Login to AWS ECR
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO}

                        # Build Docker Image with Build Args for Credentials
                        docker build -t leaflogic-app:${IMAGE_TAG} \\
                            --build-arg OPENAI_API_KEY=${OPENAI_API_KEY} \\
                            --build-arg SERPER_API_KEY=${SERPER_API_KEY} \\
                            --build-arg SENDER_PASSWORD=${SENDER_PASSWORD} \\
                            --build-arg SENDER_EMAIL=${SENDER_EMAIL} \\
                            --build-arg EXA_API_KEY=${EXA_API_KEY} .

                        # Tag Image for ECR
                        docker tag leaflogic-app:${IMAGE_TAG} ${ECR_REPO}:${IMAGE_TAG}

                        # Push to ECR
                        docker push ${ECR_REPO}:${IMAGE_TAG}
                        """
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                withCredentials([
                    string(credentialsId: 'openai_api_key', variable: 'OPENAI_API_KEY'),
                    string(credentialsId: 'serper_api_key', variable: 'SERPER_API_KEY'),
                    string(credentialsId: 'sender_password', variable: 'SENDER_PASSWORD'),
                    string(credentialsId: 'sender_email', variable: 'SENDER_EMAIL'),
                    string(credentialsId: 'exa_api_key', variable: 'EXA_API_KEY')
                ]) {
                    script {
                        sh """
                        # Authenticate with AWS ECR
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO}

                        # Stop and remove old container if it exists
                        if docker ps -q --filter "name=leaflogic-app" | grep -q .; then
                            docker stop leaflogic-app
                            docker rm leaflogic-app
                        fi

                        # Pull latest image from ECR
                        docker pull ${ECR_REPO}:${IMAGE_TAG}

                        # Run the container with environment variables
                        docker run -d --name leaflogic-app -p 5000:5000 \\
                            -e OPENAI_API_KEY=${OPENAI_API_KEY} \\
                            -e SERPER_API_KEY=${SERPER_API_KEY} \\
                            -e SENDER_PASSWORD=${SENDER_PASSWORD} \\
                            -e SENDER_EMAIL=${SENDER_EMAIL} \\
                            -e EXA_API_KEY=${EXA_API_KEY} \\
                            ${ECR_REPO}:${IMAGE_TAG}
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            echo '✅ Pipeline execution completed!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
    }
}
