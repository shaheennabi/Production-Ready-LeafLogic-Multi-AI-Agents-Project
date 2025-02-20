from flask import Flask, request, render_template, jsonify
import os
import base64
import cv2
from io import BytesIO
from PIL import Image
import numpy as np
from src.leaflogic.logger import logging
from src.leaflogic.exception import CustomException
from src.leaflogic.utils import get_label_by_index

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
YOLO_DIR = os.path.join(BASE_DIR, "yolov5")
RUNS_DIR = os.path.join(YOLO_DIR, "runs", "detect")
WEIGHTS_PATH = os.path.join(BASE_DIR, "best.pt")  # Adjust model weights path

def get_latest_exp_folder():
    try:
        if not os.path.exists(RUNS_DIR):
            return None
        exp_folders = sorted([f for f in os.listdir(RUNS_DIR) if f.startswith("exp") and f[3:].isdigit()],
                             key=lambda x: int(x[3:]), reverse=True)
        return os.path.join(RUNS_DIR, exp_folders[0]) if exp_folders else None
    except Exception as e:
        logging.error(f"Error in get_latest_exp_folder: {str(e)}")
        return None

def run_yolo_detection(input_image_path):
    try:
        os.makedirs(RUNS_DIR, exist_ok=True)
        logging.info("Running YOLO detection...")
        os.system(f"python \"{os.path.join(YOLO_DIR, 'detect.py')}\" --weights \"{WEIGHTS_PATH}\" --img 416 --conf 0.5 --source \"{input_image_path}\" --save-txt")
        return get_latest_exp_folder()
    except Exception as e:
        logging.error(f"Error running YOLO detection: {str(e)}")
        return None

def process_prediction(image_data, filename):
    try:
        image_path = os.path.join(BASE_DIR, filename)
        with open(image_path, "wb") as f:
            f.write(image_data)
        
        latest_exp_folder = run_yolo_detection(image_path)
        if not latest_exp_folder:
            return None, 'Detection failed', None
        
        output_image_path = os.path.join(latest_exp_folder, os.path.basename(image_path))
        label_folder = os.path.join(latest_exp_folder, 'labels')
        
        if not os.path.exists(label_folder):
            return "Sorry, no objects detected", None, None
        
        label_files = [f for f in os.listdir(label_folder) if f.endswith(".txt")]
        detected_labels = set()
        for label_file in label_files:
            label_path = os.path.join(label_folder, label_file)
            with open(label_path, "r") as f:
                for line in f.readlines():
                    index = int(line.strip().split()[0])
                    detected_labels.add(get_label_by_index(index))
        
        detected_text = "\n".join(detected_labels) if detected_labels else "Sorry, no objects detected"
        detected_objects_path = os.path.join(BASE_DIR, "detected_objects.txt")
        with open(detected_objects_path, "w") as txt_file:
            txt_file.write(detected_text)
        
        with open(output_image_path, "rb") as img_file:
            image_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        
        return detected_text, None, image_base64
    except Exception as e:
        logging.error(f"Error in process_prediction: {str(e)}")
        return None, str(e), None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json['image']
        image_data = base64.b64decode(data)
        labels_text, error, processed_image = process_prediction(image_data, "uploaded_image.jpg")
        if error:
            return jsonify({'error': error}), 500
        return jsonify({'labels_text': labels_text, 'image': processed_image})
    except Exception as e:
        logging.error(f"Error in predict endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
