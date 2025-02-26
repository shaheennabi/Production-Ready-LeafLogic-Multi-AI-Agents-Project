FROM python:3.10-slim

WORKDIR /app

COPY . .

# Install system dependencies for OpenCV, YOLOv5, and other libraries
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to avoid hash mismatch issues
RUN pip install --no-cache-dir --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 5000

CMD ["python3", "app.py"]