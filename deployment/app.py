import os
import base64
import glob
from src.leaflogic.exception import CustomException
from src.leaflogic.logger import logging
from src.leaflogic.utils import decodeImage, encodeImageIntoBase64
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
        deployment_path = os.path.abspath(".")  # Absolute path to deployment directory
        input_image_path = os.path.join(deployment_path, "data", clApp.filename)
        decodeImage(image, clApp.filename) #decodeImage should handle the full path construction.


        root_path = os.path.abspath("..")
        yolov5_path = os.path.join(root_path, "yolov5")
        weights_path = os.path.join(root_path, "best.pt")

        # Run YOLOv5 using absolute paths and string variables
        os.system(f"python \"{os.path.join(yolov5_path, 'detect.py')}\" --weights \"{weights_path}\" --img 416 --conf 0.5 --source \"{input_image_path}\" --save-txt")

        # Find the output image (handling potential renaming by YOLOv5)
        potential_output_paths = glob.glob(os.path.join(yolov5_path, "runs", "detect", "exp*", clApp.filename))
        if potential_output_paths:
            output_image_path = potential_output_paths[0]  # Take the first match
            print(f"YOLOv5 output found at: {output_image_path}")
        else:
            return jsonify({"error": f"YOLOv5 output not found. Check YOLOv5 runs."})

        encoded_image = encodeImageIntoBase64(output_image_path)  # Pass the file path
        if encoded_image:
            result = {"image": encoded_image}
        else:
            result = {"error": "Image encoding failed."}

        # Be cautious about deleting runs if you need them later.
        # os.system(f"rmdir /s /q \"{os.path.join(yolov5_path, 'runs')}\"") # Windows equivalent of rm -rf

        return jsonify(result)

    except (ValueError, KeyError) as e:  # Combine exception handling
        print(e)
        return jsonify({"error": "Invalid input data."})  # Return JSON error
    except Exception as e:
        print(e)
        logging.exception("An error occurred:")  # Log the full traceback
        return jsonify({"error": "An unexpected error occurred."})

@app.route("/live", methods=['GET'])
@cross_origin()
def predictLive():
    try:
        root_path = os.path.abspath("..")
        yolov5_path = os.path.join(root_path, "yolov5")
        weights_path = os.path.join(root_path, "best.pt")
        os.system(f"python \"{os.path.join(yolov5_path, 'detect.py')}\" --weights \"{weights_path}\" --img 416 --conf 0.5 --source 0")
        return "Camera starting!!"
    except Exception as e:
        print(e)
        return jsonify({"error": f"An error occurred: {e}"}) # Return JSON

if __name__ == "__main__":
    clApp = ClientApp()
    app.run(host="0.0.0.0", port=5000, debug=True)  # debug=True for development ONLY