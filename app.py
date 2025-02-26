from flask import Flask, request, jsonify, render_template
import os
import base64
import sys
import logging
import time
from src.leaflogic.logger import logging
from src.leaflogic.exception import CustomException
from src.leaflogic.utils import get_label_by_index
from taskflowai import Task
from src.leaflogic.components.agents.all_agents.web_research_agent import WebResearchAgent
from src.leaflogic.components.agents.all_agents.price_fetching_agent import PriceFetchingAgent
from src.leaflogic.utils.email_utils import SendReport2Email

app = Flask(__name__)

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
YOLO_DIR = os.path.join(BASE_DIR, "yolov5")
RUNS_DIR = os.path.join(YOLO_DIR, "runs", "detect")
WEIGHTS_PATH = os.path.join(BASE_DIR, "best.pt")
DETECTED_OBJECTS_PATH = os.path.join(BASE_DIR, "detected_objects.txt")

# Initialize email utility
send_email = SendReport2Email().send_email_via_smtp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_latest_exp_folder():
    try:
        if not os.path.exists(RUNS_DIR):
            logger.info("Runs directory does not exist.")
            return None
        exp_folders = sorted(
            [f for f in os.listdir(RUNS_DIR) if f.startswith("exp") and f[3:].isdigit()],
            key=lambda x: int(x[3:]),
            reverse=True,
        )
        latest_folder = os.path.join(RUNS_DIR, exp_folders[0]) if exp_folders else None
        logger.info(f"Latest experiment folder: {latest_folder}")
        return latest_folder
    except Exception as e:
        logger.error(f"Error in get_latest_exp_folder: {str(e)}")
        raise CustomException(sys, e)

def run_yolo_detection(input_image_path):
    try:
        os.makedirs(RUNS_DIR, exist_ok=True)
        logger.info("Running YOLO detection...")
        os.system(
            f'python "{os.path.join(YOLO_DIR, "detect.py")}" --weights "{WEIGHTS_PATH}" '
            f'--img 416 --conf 0.5 --source "{input_image_path}" --save-txt'
        )
        latest_exp_folder = get_latest_exp_folder()
        logger.info(f"YOLO detection completed. Latest experiment folder: {latest_exp_folder}")
        return latest_exp_folder
    except Exception as e:
        logger.error(f"Error running YOLO detection: {str(e)}")
        raise CustomException(sys, e)

def process_prediction(image_data, filename):
    try:
        image_path = os.path.join(BASE_DIR, filename)
        with open(image_path, "wb") as f:
            f.write(image_data)
        logger.info(f"Image saved to: {image_path}")

        latest_exp_folder = run_yolo_detection(image_path)
        if not latest_exp_folder:
            logger.error("YOLO detection failed. No experiment folder found.")
            return None, "Detection failed", None

        output_image_path = os.path.join(latest_exp_folder, os.path.basename(image_path))
        logger.info(f"Output image path: {output_image_path}")

        label_folder = os.path.join(latest_exp_folder, "labels")
        if not os.path.exists(label_folder):
            logger.info("No labels folder found. No objects detected.")
            return "Sorry, no objects detected", None, None

        detected_labels = set()
        for label_file in os.listdir(label_folder):
            if label_file.endswith(".txt"):
                label_path = os.path.join(label_folder, label_file)
                with open(label_path, "r") as f:
                    for line in f.readlines():
                        index = int(line.strip().split()[0])
                        detected_labels.add(get_label_by_index(index))
        logger.info(f"Detected labels: {detected_labels}")

        detected_text = "\n".join(detected_labels) if detected_labels else "Sorry, no objects detected"
        with open(DETECTED_OBJECTS_PATH, "w") as txt_file:
            txt_file.write(detected_text)
        logger.info(f"Detected objects saved to: {DETECTED_OBJECTS_PATH}")

        with open(output_image_path, "rb") as img_file:
            image_base64 = base64.b64encode(img_file.read()).decode("utf-8")
        logger.info("Output image encoded to base64.")

        return detected_text, None, image_base64
    except Exception as e:
        logger.error(f"Error in process_prediction: {str(e)}")
        raise CustomException(sys, e)

def read_detected_objects(file_path):
    if not os.path.exists(file_path):
        logger.info(f"File not found: {file_path}")
        return []
    try:
        with open(file_path, "r") as file:
            detected_objects = [line.strip() for line in file.readlines() if line.strip()]
        logger.info(f"Detected objects read from file: {detected_objects}")
        return detected_objects
    except Exception as e:
        logger.error(f"Error reading detected objects: {str(e)}")
        raise CustomException(sys, e)

def execute_research_and_report(plant_names):
    research_results = {}
    try:
        if not plant_names:
            return research_results
        for plant_name in plant_names:
            research_results[plant_name] = {
                "general": research_overall_web(plant_name),
                "health": research_health(plant_name),
                "season": research_season(plant_name),
                "price": research_price(plant_name),
            }
        return research_results
    except Exception as e:
        logger.error(f"Error in execute_research_and_report: {str(e)}")
        raise Exception(f"Error in execute_research_and_report: {str(e)}")

def generate_summarized_report(research_results):
    try:
        if not research_results:
            return "No research results to summarize."
        summarized_report = "<h2>🌿 Plant Research Summary 🌿</h2><br>\n"
        for plant, results in research_results.items():
            summarized_report += f"<h3>🌱 {plant.capitalize()}</h3><br>\n"
            summarized_report += f"<h4>📌 General Information</h4><br>\n<p>{'<br>'.join(str(results.get('general', 'No data available')).splitlines())}</p><br>\n"
            summarized_report += "<hr>\n"
            summarized_report += f"<h4>🩺 Health Benefits & Risks</h4><br>\n<p>{'<br>'.join(str(results.get('health', 'No data available')).splitlines())}</p><br>\n"
            summarized_report += "<hr>\n"
            summarized_report += f"<h4>🌤 Growing Season & Conditions</h4><br>\n<p>{'<br>'.join(str(results.get('season', 'No data available')).splitlines())}</p><br>\n"
            summarized_report += "<hr>\n"
            summarized_report += f"<h4>💰 Market Prices & Trends</h4><br>\n<p>{'<br>'.join(str(results.get('price', 'No data available')).splitlines())}</p><br>\n"
            summarized_report += "<hr>\n"
        return summarized_report
    except Exception as e:
        logger.error(f"Error in generate_summarized_report: {str(e)}")
        raise Exception(f"Error in generate_summarized_report: {str(e)}")

def research_overall_web(plant_name: str):
    try:
        agent = WebResearchAgent.initialize_web_research_agent()
        task = Task.create(
            agent=agent,
            context=f"Plant Name: {plant_name}",
            instruction=(
                f"Research {plant_name} and provide details on:\n"
                f"- Scientific classification, origin, and regions\n"
                f"- Uses, benefits, and growth conditions\n"
                f"- Pests, diseases, and economic significance\n"
                f"- Provide relevant images related to {plant_name}(![Description](https://full-image-url))\n"
            ),
        )
        return task
    except Exception as e:
        logger.error(f"Error in research_overall_web for {plant_name}: {e}")
        raise Exception(f"Error in research_overall_web for {plant_name}: {e}")

def research_health(plant_name: str):
    try:
        agent = WebResearchAgent.initialize_web_research_agent()
        task = Task.create(
            agent=agent,
            context=f"Plant: {plant_name}",
            instruction=(
                f"Research health aspects of {plant_name}, including:\n"
                f"- Benefits & medicinal uses\n"
                f"- Risks & toxicity\n"
                f"- Nutritional value\n"
                f"- Traditional remedies\n"
                f"Provide structured, referenced insights."
            ),
        )
        return task
    except Exception as e:
        logger.error(f"Error in research_health: {e}")
        raise Exception(f"Error in research_health: {e}")

def research_season(plant_name: str):
    try:
        agent = WebResearchAgent.initialize_web_research_agent()
        task = Task.create(
            agent=agent,
            context=f"Plant: {plant_name}",
            instruction=(
                f"Research {plant_name}'s optimal growth conditions:\n"
                f"- Planting & harvesting seasons\n"
                f"- Climate, temperature, humidity\n"
                f"- Soil, nutrients, fertilizers\n"
                f"- Best farming practices\n"
                f"- Off-season storage & uses\n"
                f"Provide expert-backed agricultural insights."
            ),
        )
        return task
    except Exception as e:
        logger.error(f"Error in research_season: {e}")
        raise Exception(f"Error in research_season: {e}")

def research_price(plant_name: str):
    try:
        agent = PriceFetchingAgent.initialize_price_fetching_agent(query=plant_name)
        task = Task.create(
            agent=agent,
            context=f"Plant: {plant_name}",
            instruction=(
                f"Fetch {plant_name} market prices:\n"
                f"- Online price rates\n"
                f"- Cheapest price {plant_name} is available at\n"
                f"- Identify the **lowest available price** and where it is found\n"
                f"Provide accurate, up-to-date market data."
            ),
        )
        return task
    except Exception as e:
        logger.error(f"Error in research_price: {e}")
        raise Exception(f"Error in research_price: {e}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json["image"]
        image_data = base64.b64decode(data)
        logger.info("Image data received and decoded.")

        labels_text, error, processed_image = process_prediction(image_data, "uploaded_image.jpg")
        if error:
            logger.error(f"Error in process_prediction: {error}")
            return jsonify({"error": error, "image": None}), 500

        detected_objects = read_detected_objects(DETECTED_OBJECTS_PATH)
        logger.info(f"Detected objects: {detected_objects}")

        research_started = False
        research_results = {}
        summarized_report = "No detected objects to generate a report."
        if detected_objects:
            logger.info("Starting research and report generation.")
            research_started = True
            try:
                research_results = execute_research_and_report(detected_objects)
                summarized_report = generate_summarized_report(research_results)
                logger.info("Research and report generation completed.")
            except Exception as e:
                logger.error(f"Error in research and report generation: {str(e)}")

        # Convert Task objects to strings for serialization
        serialized_research_results = {
            plant: {key: str(value) for key, value in data.items()}
            for plant, data in research_results.items()
        }

        return jsonify(
            {
                "labels_text": labels_text,
                "image": processed_image,
                "detected_objects": detected_objects,
                "research_results": serialized_research_results,
                "summarized_report": summarized_report,
                "research_started": research_started,
            }
        )
    except Exception as e:
        logger.error(f"Error in predict endpoint: {str(e)}")
        return jsonify({"error": str(e), "image": None}), 500

@app.route("/send-report", methods=["POST"])
def send_report():
    try:
        data = request.json
        email = data.get("email")
        summarized_report_html = data.get("summarized_report")

        if not email or not summarized_report_html:
            logger.error("Email or summarized report missing in request.")
            return {"error": "Email and summarized report are required."}, 400

        # Convert HTML to plain text for compatibility with send_email
        summarized_report_text = summarized_report_html.replace('<h2>', '\n').replace('</h2>', '\n') \
            .replace('<h3>', '\n').replace('</h3>', '\n') \
            .replace('<h4>', '\n').replace('</h4>', '\n') \
            .replace('<p>', '').replace('</p>', '\n') \
            .replace('<br>', '\n').replace('<hr>', '\n---\n') \
            .replace('<strong>', '*').replace('</strong>', '*') \
            .replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        subject = "Your Summarized Report from Leaflogic"
        body = f"Here is your summarized report:\n\n{summarized_report_text}"
        logger.info(f"Sending email to: {email}")

        if send_email(email, subject, body):  # No is_html parameter
            logger.info("Email sent successfully.")
            return {"message": "Report sent successfully!"}, 200
        else:
            logger.error("Failed to send email.")
            return {"error": "Failed to send the report."}, 500
    except Exception as e:
        logger.error(f"Error in send_report endpoint: {str(e)}")
        return {"error": str(e)}, 500

@app.route("/end-program", methods=["POST"])
def end_program():
    try:
        logger.info("Received request to shut down the application.")
        def shutdown_server():
            time.sleep(1)
            logger.info("Shutting down server.")
            os._exit(0)
        import threading
        threading.Thread(target=shutdown_server).start()
        return {"message": "Server shutting down..."}, 200
    except Exception as e:
        logger.error(f"Error in end_program endpoint: {str(e)}")
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)