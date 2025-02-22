from flask import Flask, request, render_template
import os
import base64
from src.leaflogic.logger import logging
from src.leaflogic.exception import CustomException
from src.leaflogic.utils import get_label_by_index
from taskflowai import Task
from src.leaflogic.components.agents.all_agents.web_research_agent import WebResearchAgent
from src.leaflogic.components.agents.all_agents.price_fetching_agent import PriceFetchingAgent
from src.leaflogic.components.agents.all_agents.report_generator_agent import ReportGeneratorAgent
from src.leaflogic.utils  import SendReport2Email

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
YOLO_DIR = os.path.join(BASE_DIR, "yolov5")
RUNS_DIR = os.path.join(YOLO_DIR, "runs", "detect")
WEIGHTS_PATH = os.path.join(BASE_DIR, "best.pt")  # Adjust model weights path

# Function to get the latest experiment folder
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

# Function to run YOLO detection
def run_yolo_detection(input_image_path):
    try:
        os.makedirs(RUNS_DIR, exist_ok=True)
        logging.info("Running YOLO detection...")
        os.system(f"python \"{os.path.join(YOLO_DIR, 'detect.py')}\" --weights \"{WEIGHTS_PATH}\" --img 416 --conf 0.5 --source \"{input_image_path}\" --save-txt")
        return get_latest_exp_folder()
    except Exception as e:
        logging.error(f"Error running YOLO detection: {str(e)}")
        return None

# Function to process prediction
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

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json['image']
        image_data = base64.b64decode(data)
        labels_text, error, processed_image = process_prediction(image_data, "uploaded_image.jpg")
        if error:
            return {'error': error}, 500
        
        # Trigger research tasks
        detected_objects = read_detected_objects(os.path.join(BASE_DIR, "detected_objects.txt"))
        if detected_objects:
            research_results = execute_research_and_report(detected_objects)
            summarized_report = generate_summarized_report(research_results)
        else:
            research_results = {}
            summarized_report = "No detected objects to generate a report."
        
        return {
            'labels_text': labels_text,
            'image': processed_image,
            'research_results': research_results,
            'summarized_report': summarized_report
        }
    except Exception as e:
        logging.error(f"Error in predict endpoint: {str(e)}")
        return {'error': str(e)}, 500

# Function to read detected objects
def read_detected_objects(file_path):
    """Reads detected crop/plant names from the file."""
    if not os.path.exists(file_path):
        logging.info(f"File not found: {file_path}")
        return []
    
    try:
        with open(file_path, "r") as file:
            detected_objects = [line.strip() for line in file.readlines() if line.strip()]
        return detected_objects
    except Exception as e:
        logging.info(f"Error reading detected objects: {str(e)}")
        return []

# Function to execute research and generate report
def execute_research_and_report(detected_objects):
    """Executes research and generates a report for detected objects."""
    research_results = {}
    try:
        if not detected_objects:
            logging.info("No detected objects to research.")
            return research_results
        
        for plant_name in detected_objects:
            # Perform research tasks
            research_results[plant_name] = {
                "general": research_overall_web(plant_name),
                "health": research_health(plant_name),
                "season": research_season(plant_name),
                "price": research_price(plant_name)
            }
        
        return research_results
    except Exception as e:
        logging.error(f"Error in execute_research_and_report: {str(e)}")
        return research_results

# Function to generate summarized report
def generate_summarized_report(research_results):
    """Generates a summarized report from research results."""
    try:
        if not research_results:
            return "No research results to summarize."
        
        summarized_report = "Summarized Report:\n\n"
        for plant, results in research_results.items():
            summarized_report += f"**{plant}**\n"
            summarized_report += f"- General Information: {results['general']}\n"
            summarized_report += f"- Health Benefits: {results['health']}\n"
            summarized_report += f"- Growing Season: {results['season']}\n"
            summarized_report += f"- Market Prices: {results['price']}\n\n"
        
        return summarized_report
    except Exception as e:
        logging.error(f"Error in generate_summarized_report: {str(e)}")
        return "Error generating summarized report."

# Research functions
def research_overall_web(plant_name):
    """Research general details about the plant."""
    try:
        task = Task.create(
            agent=WebResearchAgent.initialize_web_research_agent(),
            context=f"Plant Name: {plant_name}",
            instruction=(
                f"Research detailed information on {plant_name} including:\n"
                f"- Scientific name\n"
                f"- History and origin\n"
                f"- Major growing regions\n"
                f"- Relevant images (formatted as: ![Description](https://full-image-url))"
            )
        )
        logging.info(f"Successfully created general research task for {plant_name}.")
        return task.result  # Assuming Task.result contains the research output
    except Exception as e:
        logging.info(f"Failed to create general research task for {plant_name}: {str(e)}")
        raise CustomException(f"Error creating general research task: {str(e)}")

def research_health(plant_name):
    """Research health-related information about the plant."""
    try:
        task = Task.create(
            agent=WebResearchAgent.initialize_web_research_agent(),
            context=f"Plant Name: {plant_name}",
            instruction=(
                f"Research health aspects of {plant_name}, including:\n"
                f"- Health benefits\n"
                f"- Potential risks & side effects\n"
                f"- Nutritional value (vitamins & minerals)\n"
                f"- Medicinal uses"
            )
        )
        logging.info(f"Successfully created health research task for {plant_name}.")
        return task.result  # Assuming Task.result contains the research output
    except Exception as e:
        logging.info(f"Failed to create health research task for {plant_name}: {str(e)}")
        raise CustomException(f"Error creating health research task: {str(e)}")

def research_season(plant_name):
    """Research seasonal growth and farming details."""
    try:
        task = Task.create(
            agent=WebResearchAgent.initialize_web_research_agent(),
            context=f"Plant Name: {plant_name}",
            instruction=(
                f"Research farming aspects of {plant_name}, including:\n"
                f"- Best seasons for growth\n"
                f"- Climate & temperature requirements\n"
                f"- Soil & nutrients needed\n"
                f"- Farming & growth process\n"
                f"- Alternative uses in off-seasons"
            )
        )
        logging.info(f"Successfully created seasonal research task for {plant_name}.")
        return task.result  # Assuming Task.result contains the research output
    except Exception as e:
        logging.info(f"Failed to create seasonal research task for {plant_name}: {str(e)}")
        raise CustomException(f"Error creating seasonal research task: {str(e)}")

def research_price(plant_name):
    """Research market price details of the plant."""
    try:
        task = Task.create(
            agent=PriceFetchingAgent.initialize_price_fetching_agent(),
            context=f"Plant Name: {plant_name}",
            instruction=(
                f"Research market prices of {plant_name}, including:\n"
                f"- Price comparison across different markets\n"
                f"- Price per kg vs. lb\n"
                f"- Location-based price variations\n"
                f"- Quality vs. price analysis"
            )
        )
        logging.info(f"Successfully created price research task for {plant_name}.")
        return task.result  # Assuming Task.result contains the research output
    except Exception as e:
        logging.info(f"Failed to create price research task for {plant_name}: {str(e)}")
        raise CustomException(f"Error creating price research task: {str(e)}")






# Route to handle email submission
@app.route('/send-report', methods=['POST'])
def send_report():
    try:
        data = request.json
        email = data.get('email')
        summarized_report = data.get('summarized_report')
        
        if not email or not summarized_report:
            return {'error': 'Email and summarized report are required.'}, 400
        
        # Send the email
        subject = "Your Summarized Report from Leaflogic"
        body = f"Here is your summarized report:\n\n{summarized_report}"
        
        if send_email_via_smtp(email, subject, body):
            return {'message': 'Report sent successfully!'}, 200
        else:
            return {'error': 'Failed to send the report.'}, 500
    except Exception as e:
        logging.error(f"Error in send_report endpoint: {str(e)}")
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)