# Update system packages to ensure compatibility and security
sudo apt update && sudo apt upgrade -y

# Install AWS CLI to interact with AWS services like ECR
# Install unzip utility for extracting AWS CLI installer
sudo apt install -y unzip
# Download AWS CLI v2 binary
curl "https://awscli.amazonaws.com/awscli-exe-linux-x64.zip" -o "awscliv2.zip"
# Extract the installer
unzip awscliv2.zip
# Install AWS CLI to /usr/local/bin/aws
sudo ./aws/install
# Verify AWS CLI installation
aws --version
# Configure AWS CLI with your credentials (run interactively, enter IAM keys)
aws configure

# Install Docker to build and run Flask app containers
# Install required packages for Docker setup
sudo apt install -y ca-certificates curl gnupg lsb-release
# Create directory for Docker's GPG key
sudo mkdir -m 0755 -p /etc/apt/keyrings
# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
# Set up Docker repository for Ubuntu
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
# Update apt package index with Docker repository
sudo apt update
# Install Docker Engine and related tools
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
# Add ubuntu user to docker group to run Docker without sudo
sudo usermod -aG docker ubuntu
# Apply group changes (alternative to logout/login; run newgrp in current session)
newgrp docker
# Test Docker installation
docker --version
docker run hello-world

# Install Jenkins for CI/CD automation
# Install Java (required for Jenkins)
sudo apt install -y openjdk-11-jdk
# Download Jenkins GPG key and add to trusted keyring (modern method)
wget -q -O /etc/apt/trusted.gpg.d/jenkins.io.key https://pkg.jenkins.io/debian-stable/jenkins.io.key
# Add Jenkins repository to sources list
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
# Update apt package index with Jenkins repository
sudo apt update
# Install Jenkins
sudo apt install -y jenkins
# Start Jenkins service
sudo systemctl start jenkins
# Enable Jenkins to start on boot
sudo systemctl enable jenkins
# Check Jenkins service status
sudo systemctl status jenkins

# Post-installation: Log out and back in to apply Docker group changes
# Exit current session
exit
# Reconnect to EC2 (replace /path/to/ with your local path to leaflogic.pem)
ssh -i /path/to/leaflogic.pem ubuntu@3.85.221.27

# Verify all installations after reconnecting
aws --version
docker --version
sudo systemctl status jenkins

# Configure Jenkins (manual steps via browser)
# Access Jenkins at http://3.85.221.27:8080
# Get initial admin password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
# Follow setup wizard: Install suggested plugins, create admin user
# Install additional plugins via Manage Jenkins > Manage Plugins:
# - GitHub Integration
# - Docker Pipeline
# - Amazon ECR
# - Pipeline

# Add AWS and API credentials to Jenkins (manual via Jenkins UI)
# Navigate: Manage Jenkins > Manage Credentials > System > Global Credentials > Add Credentials
# Add each as 'Secret text' with respective IDs:
# - ID: aws_access_key_id, Secret: <your-aws-access-key-id>
# - ID: aws_secret_access_key, Secret: <your-aws-secret-access-key>
# - ID: openai_api_key, Secret: <your-openai-api-key>
# - ID: serper_api_key, Secret: <your-serper-api-key>
# - ID: sender_password, Secret: <your-sender-password>
# - ID: sender_email, Secret: <your-sender-email>
# - ID: exa_api_key, Secret: <your-exa-api-key>

# Authenticate Docker with ECR (replace with your ECR URI and region)
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# Create Jenkins Pipeline (manual via Jenkins UI)
# New Item > Pipeline > Name: LeafLogic-CICD > Pipeline script:
# Paste this updated Jenkinsfile:
pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'  # AWS region for ECR and deployment
        ECR_REPO = 'your ecr repo uri'  # Your ECR repository URI
        IMAGE_TAG = 'latest'  # Tag for the Docker image
    }

    stages {
        stage('Checkout Code') {
            steps {
                # Pull code from your GitHub repository
                git url: 'https://github.com/your project repo url', branch: 'main'
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
                        sh '''
                        # Configure AWS CLI with credentials
                        aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                        aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                        aws configure set region $AWS_REGION

                        # Login to AWS ECR
                        aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO

                        # Build Docker image with API keys as build arguments
                        docker build -t leaflogic-app:$IMAGE_TAG \
                            --build-arg OPENAI_API_KEY="$OPENAI_API_KEY" \
                            --build-arg SERPER_API_KEY="$SERPER_API_KEY" \
                            --build-arg SENDER_PASSWORD="$SENDER_PASSWORD" \
                            --build-arg SENDER_EMAIL="$SENDER_EMAIL" \
                            --build-arg EXA_API_KEY="$EXA_API_KEY" \
                            .

                        # Tag the image for ECR
                        docker tag leaflogic-app:$IMAGE_TAG $ECR_REPO:$IMAGE_TAG

                        # Push the image to ECR
                        docker push $ECR_REPO:$IMAGE_TAG
                        '''
                    }
                }
            }
        }

        stage('Deploy to EC2') {
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
                        sh '''
                        # Authenticate with ECR
                        aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO

                        # Stop and remove any existing container named leaflogic-app
                        docker stop leaflogic-app || true
                        docker rm leaflogic-app || true

                        # Pull the latest image from ECR
                        docker pull $ECR_REPO:$IMAGE_TAG

                        # Run the container with API keys as environment variables
                        docker run -d --name leaflogic-app -p 80:5000 \
                            -e OPENAI_API_KEY="$OPENAI_API_KEY" \
                            -e SERPER_API_KEY="$SERPER_API_KEY" \
                            -e SENDER_PASSWORD="$SENDER_PASSWORD" \
                            -e SENDER_EMAIL="$SENDER_EMAIL" \
                            -e EXA_API_KEY="$EXA_API_KEY" \
                            $ECR_REPO:$IMAGE_TAG
                        '''
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

# Ensure Docker permissions for Jenkins
# Check Docker socket permissions
ls -l /var/run/docker.sock
# Add Jenkins user to docker group
sudo usermod -aG docker jenkins
# Restart Jenkins to apply changes
sudo systemctl restart jenkins
# Verify Docker works with Jenkins user
sudo -u jenkins docker ps



# Required GitHub Repository Secrets (add via Jenkins UI)
# Navigate: Manage Jenkins > Manage Credentials > System > Global Credentials > Add Credentials
# Add each as 'Secret text' with respective IDs:
# - ID: aws_access_key_id, Secret: Your AWS IAM access key
# - ID: aws_secret_access_key, Secret: Your AWS IAM secret key
# - ID: openai_api_key, Secret: Your OpenAI API key
# - ID: serper_api_key, Secret: Your Serper API key
# - ID: sender_password, Secret: Your email sender password
# - ID: sender_email, Secret: Your email sender address
# - ID: exa_api_key, Secret: Your Exa API key
