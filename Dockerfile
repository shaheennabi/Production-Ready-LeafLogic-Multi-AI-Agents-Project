FROM python:3.10-slim

WORKDIR /app

COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt



# Expose the port Streamlit uses
EXPOSE 5000

CMD ["python3", "app.py"]