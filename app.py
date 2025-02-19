import os
import base64
import glob
from src.leaflogic.exception import CustomException  # Assuming you have this
from src.leaflogic.logger import logging  # Assuming you have this
from src.leaflogic.utils import decodeImage, encodeImageIntoBase64  # Assuming you have this
from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=['POST','GET'])
@cross_origin()
def predictRoute():
    try:
        image = request.json['image']
        clApp = ClientApp()
        input_image_path = os.path.join("data", clApp.filename)  # Relative path

        decodeImage(image, clApp.filename)

        yolov5_path = "yolov5"  # Relative path (in the same directory)
        weights_path = "best.pt"  # Relative path (in the same directory)

        output_dir = os.path.join(yolov5_path, "runs", "detect", "exp")
        os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist

        os.system(f"python \"{os.path.join(yolov5_path, 'detect.py')}\" --weights \"{weights_path}\" --img 416 --conf 0.5 --source \"{input_image_path}\" --save-txt --save-dir \"{output_dir}\"")

        output_image_path = os.path.join(output_dir, clApp.filename)

        if os.path.exists(output_image_path):
            encoded_image = encodeImageIntoBase64(output_image_path)
            if encoded_image:
                result = {"image": encoded_image}
            else:
                result = {"error": "Image encoding failed."}
        else:
            result = {"error": "YOLOv5 output not found."}

        return jsonify(result)

    except (ValueError, KeyError) as e:
        logging.exception(f"Invalid input data: {e}") # Include exception info
        return jsonify({"error": f"Invalid input data: {str(e)}"})
    except FileNotFoundError as e:
        logging.exception(f"File not found: {e}") # Include exception info
        return jsonify({"error": f"File not found: {str(e)}"})
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}") # Include exception info
        return jsonify({"error": "An unexpected error occurred. Please check the logs."})

@app.route("/live", methods=['GET'])
@cross_origin()
def predictLive():
    try:
        yolov5_path = "yolov5"  # Relative path
        weights_path = "best.pt"  # Relative path
        os.system(f"python \"{os.path.join(yolov5_path, 'detect.py')}\" --weights \"{weights_path}\" --img 416 --conf 0.5 --source 0")
        return "Camera starting!!"
    except Exception as e:
        logging.exception(f"An error occurred in predictLive: {e}")
        return jsonify({"error": f"An error occurred: {str(e)}"})

if __name__ == "__main__":
    clApp = ClientApp()
    app.run(host="0.0.0.0", port=5000, debug=True)  # debug=True for development ONLY
