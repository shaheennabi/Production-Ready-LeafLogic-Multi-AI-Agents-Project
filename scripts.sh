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

# Add AWS credentials to Jenkins (manual via Jenkins UI)
# Navigate: Manage Jenkins > Manage Credentials > System > Global Credentials > Add Credentials
# Kind: AWS Credentials
# ID: aws-credentials
# Access Key ID: <your-aws-access-key-id>
# Secret Access Key: <your-aws-secret-access-key>

# Authenticate Docker with ECR (replace with your ECR URI and region)
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# Create Jenkins Pipeline (manual via Jenkins UI)
# New Item > Pipeline > Name: LeafLogic-CICD > Pipeline script:
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/yourusername/leaflogic-project.git', branch: 'main'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    def app = docker.build("leaflogic-app:${env.BUILD_NUMBER}")
                }
            }
        }
        stage('Push to ECR') {
            steps {
                script {
                    docker.withRegistry('https://123456789012.dkr.ecr.us-east-1.amazonaws.com', 'ecr:us-east-1:aws-credentials') {
                        docker.image("leaflogic-app:${env.BUILD_NUMBER}").push()
                        docker.image("leaflogic-app:${env.BUILD_NUMBER}").push('latest')
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                docker stop leaflogic-app || true
                docker rm leaflogic-app || true
                docker run -d --name leaflogic-app -p 80:5000 \
                -e OPENAI_API_KEY=$OPENAI_API_KEY \
                -e SERPER_API_KEY=$SERPER_API_KEY \
                -e EXA_API_KEY=$EXA_API_KEY \
                -e SENDER_PASSWORD=$SENDER_PASSWORD \
                -e SENDER_EMAIL=$SENDER_EMAIL \
                123456789012.dkr.ecr.us-east-1.amazonaws.com/leaflogic-app:latest
                '''
            }
        }
    }
}

# Required GitHub Repository Secrets (add via Jenkins UI or GitHub Secrets)
# Navigate: Manage Jenkins > Manage Credentials > System > Global Credentials > Add Credentials
# Add each as 'Secret text' with respective IDs
# AWS_ACCESS_KEY_ID: Your AWS IAM access key
# AWS_SECRET_ACCESS_KEY: Your AWS IAM secret key
# AWS_DEFAULT_REGION: e.g., us-east-1
# AWS_ECR_REPO_URI: e.g., 123456789012.dkr.ecr.us-east-1.amazonaws.com/leaflogic-app
# OPENAI_API_KEY: Your OpenAI API key
# SERPER_API_KEY: Your Serper API key
# EXA_API_KEY: Your Exa API key
# SENDER_PASSWORD: Your email sender password
# SENDER_EMAIL: Your email sender address
# SSH_KEY: Your private SSH key (if needed for GitHub access)

# Configure GitHub Webhook (manual via GitHub UI)
# In your GitHub repo > Settings > Webhooks > Add Webhook
# Payload URL: http://3.85.221.27:8080/github-webhook/
# Content type: application/json
# Events: Select "Push events"
# Save the webhook

# Ensure Docker permissions for Jenkins
# Check Docker socket permissions
ls -l /var/run/docker.sock
# Add Jenkins user to docker group
sudo usermod -aG docker jenkins
# Restart Jenkins to apply changes
sudo systemctl restart jenkins
# Verify Docker works with Jenkins user
sudo -u jenkins docker ps
