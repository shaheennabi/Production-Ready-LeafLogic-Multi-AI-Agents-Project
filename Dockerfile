# Use Python 3.10 slim as the base image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy all project files to /app in the container
COPY . .

# Install system dependencies for OpenCV and YOLOv5
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    gcc \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to ensure compatibility with Python packages
RUN pip install --no-cache-dir --upgrade pip

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define build arguments for API keys and email credentials
ARG OPENAI_API_KEY
ARG SERPER_API_KEY
ARG EXA_API_KEY
ARG SENDER_PASSWORD
ARG SENDER_EMAIL

# Set environment variables from build arguments
ENV OPENAI_API_KEY=${OPENAI_API_KEY} \
    SERPER_API_KEY=${SERPER_API_KEY} \
    EXA_API_KEY=${EXA_API_KEY} \
    SENDER_PASSWORD=${SENDER_PASSWORD} \
    SENDER_EMAIL=${SENDER_EMAIL}

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run the Flask app
CMD ["python3", "app.py", "--server.port=5000", "--server.address=0.0.0.0"]





