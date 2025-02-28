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
                    string(credentialsId: 'aws_access_key_id', variable: 'aws_access_key_id'),
                    string(credentialsId: 'aws_secret_access_key', variable: 'aws_secret_access_key'),
                    string(credentialsId: 'openai_api_key', variable: 'openai_api_key'),
                    string(credentialsId: 'serper_api_key', variable: 'serper_api_key'),
                    string(credentialsId: 'sender_password', variable: 'sender_password'),
                    string(credentialsId: 'sender_email', variable: 'sender_email'),
                    string(credentialsId: 'exa_api_key', variable: 'exa_api_key')
                ]) {
                    script {
                        sh '''
                        # Configure AWS CLI
                        aws configure set aws_access_key_id $aws_access_key_id
                        aws configure set aws_secret_access_key $aws_secret_access_key
                        aws configure set region $AWS_REGION

                        # Login to AWS ECR
                        aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO

                        # Build Docker Image with Build Args for Credentials
                        docker build -t leaflogic-app:${IMAGE_TAG} \
                        --build-arg OPENAI_API_KEY=$openai_api_key \
                        --build-arg SERPER_API_KEY=$serper_api_key \
                        --build-arg SENDER_PASSWORD=$sender_password \
                        --build-arg SENDER_EMAIL=$sender_email \
                        --build-arg EXA_API_KEY=$exa_api_key .

                        # Tag Image for ECR
                        docker tag leaflogic-app:${IMAGE_TAG} $ECR_REPO:${IMAGE_TAG}

                        # Push to ECR
                        docker push $ECR_REPO:${IMAGE_TAG}
                        '''
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                script {
                    sh '''
                    # Authenticate with ECR
                    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 445567117176.dkr.ecr.us-east-1.amazonaws.com

                    # Stop and remove old container if it exists
                    docker ps -q --filter "name=leaflogic-app" | grep -q . && docker stop leaflogic-app && docker rm leaflogic-app || true

                    # Pull latest image from ECR
                    docker pull 445567117176.dkr.ecr.us-east-1.amazonaws.com/leaflogic:latest

                    # Run the container
                    docker run -d --name leaflogic-app -p 5000:5000 \
                    -e OPENAI_API_KEY=$openai_api_key \
                    -e SERPER_API_KEY=$serper_api_key \
                    -e SENDER_PASSWORD=$sender_password \
                    -e SENDER_EMAIL=$sender_email \
                    -e EXA_API_KEY=$exa_api_key \
                    445567117176.dkr.ecr.us-east-1.amazonaws.com/leaflogic:latest
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
