from flask import Flask, request, jsonify, render_template
import os
import base64
import sys
import logging
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
WEIGHTS_PATH = os.path.join(BASE_DIR, "best.pt")  # Path to model weights
DETECTED_OBJECTS_PATH = os.path.join(BASE_DIR, "detected_objects.txt")  # Path to detected objects file

# Initialize email utility
send_email = SendReport2Email().send_email_via_smtp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to get the latest experiment folder
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

# Function to run YOLO detection
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

# Function to process prediction
def process_prediction(image_data, filename):
    try:
        # Save the uploaded image
        image_path = os.path.join(BASE_DIR, filename)
        with open(image_path, "wb") as f:
            f.write(image_data)
        logger.info(f"Image saved to: {image_path}")

        # Run YOLO detection
        latest_exp_folder = run_yolo_detection(image_path)
        if not latest_exp_folder:
            logger.error("YOLO detection failed. No experiment folder found.")
            return None, "Detection failed", None

        # Get the output image path
        output_image_path = os.path.join(latest_exp_folder, os.path.basename(image_path))
        logger.info(f"Output image path: {output_image_path}")

        # Read detected labels
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

        # Save detected objects to a text file
        detected_text = "\n".join(detected_labels) if detected_labels else "Sorry, no objects detected"
        with open(DETECTED_OBJECTS_PATH, "w") as txt_file:
            txt_file.write(detected_text)
        logger.info(f"Detected objects saved to: {DETECTED_OBJECTS_PATH}")

        # Encode the output image to base64
        with open(output_image_path, "rb") as img_file:
            image_base64 = base64.b64encode(img_file.read()).decode("utf-8")
        logger.info("Output image encoded to base64.")

        return detected_text, None, image_base64
    except Exception as e:
        logger.error(f"Error in process_prediction: {str(e)}")
        raise CustomException(sys, e)

# Function to read detected objects from the text file
def read_detected_objects(file_path):
    """Reads detected crop/plant names from the file."""
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
    """Executes research tasks and generates a structured report for each plant.

    Args:
        plant_names (list): A list of plant names to research.

    Returns:
        dict: Research results categorized by plant name.
    """
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
        raise Exception(f"Error in execute_research_and_report: {str(e)}")





















def generate_summarized_report(research_results):
    """Generates a structured and easy-to-read summarized report from research results.

    Args:
        research_results (dict): A dictionary containing research data for each plant.

    Returns:
        str: A formatted summary report of the research.
    """
    try:
        if not research_results:
            return "No research results to summarize."

        summarized_report = "🌿 **Plant Research Summary** 🌿\n\n"
        
        for plant, results in research_results.items():
            summarized_report += f"🌱 **{plant.capitalize()}**\n"
            summarized_report += f"📌 **General Information:** {results.get('general', 'No data available')}\n"
            summarized_report += f"🩺 **Health Benefits & Risks:** {results.get('health', 'No data available')}\n"
            summarized_report += f"🌤 **Growing Season & Conditions:** {results.get('season', 'No data available')}\n"
            summarized_report += f"💰 **Market Prices & Trends:** {results.get('price', 'No data available')}\n"
            summarized_report += "-" * 50 + "\n\n"

        return summarized_report

    except Exception as e:
        raise Exception(f"Error in generate_summarized_report: {str(e)}")




















def research_overall_web(plant_name: str):
    """
    Conducts an in-depth web research on the given plant and gathers comprehensive details.

    Goal:
    - To collect and summarize high-quality information about a plant species from trusted web sources.

    Attributes:
    - Scientific Name: The botanical classification of the plant.
    - History & Origin: Where the plant originates from, its historical significance, and domestication details.
    - Major Growing Regions: Countries and climates where the plant thrives.
    - Uses & Benefits: Agricultural, medicinal, nutritional, and industrial applications.
    - Growth Conditions: Soil type, temperature, humidity, and watering requirements.
    - Common Pests & Diseases: Typical threats and prevention strategies.
    - Cultural & Economic Significance: Traditional and commercial importance in different regions.
    - Relevant Images: Well-labeled images of the plant formatted as ![Description](https://full-image-url).

    Returns:
    - A structured research task that gathers this information using an AI-powered web research agent.

    Raises:
    - Exception: If the research process encounters an error.
    """

    try:
        # Initialize the research agent
        agent = WebResearchAgent.initialize_web_research_agent()

        # Create and execute the research task
        task = Task.create(
            agent=agent,
            context=f"Plant Name: {plant_name}",
            instruction=(
                f"Conduct thorough research on {plant_name} and provide structured information on:\n"
                f"- **Scientific Name**: Botanical classification.\n"
                f"- **History & Origin**: Historical significance and domestication.\n"
                f"- **Major Growing Regions**: Suitable climates and geographical distribution.\n"
                f"- **Uses & Benefits**: Applications in agriculture, medicine, and industry.\n"
                f"- **Growth Conditions**: Soil type, temperature, humidity, and watering needs.\n"
                f"- **Common Pests & Diseases**: Common threats and mitigation strategies.\n"
                f"- **Cultural & Economic Significance**: Importance in different regions.\n"
                f"- **Relevant Images**: Provide high-quality images formatted as ![Description](https://full-image-url).\n"
            ),
        )

        return task

    except Exception as e:
        raise Exception(f"Error in research_overall_web for {plant_name}: {str(e)}")













def research_health(plant_name: str):
    """Research health-related information about the plant.

    Args:
        plant_name (str): The name of the plant to research.

    Returns:
        Task: The research task instance containing health-related insights.
    """
    try:
        agent = WebResearchAgent.initialize_web_research_agent()

        task = Task.create(
            agent=agent,
            context=f"Plant Name: {plant_name}",
            instruction=(
                f"Research the health aspects of {plant_name}, including:\n"
                f"- Key health benefits and medicinal uses.\n"
                f"- Potential risks, side effects, and toxicity levels.\n"
                f"- Nutritional value (vitamins, minerals, and compounds).\n"
                f"- Common medical or traditional remedies using {plant_name}.\n"
                f"- Scientific studies or expert insights supporting health claims.\n"
                f"Provide structured and well-referenced information."
            ),
        )

        return task

    except Exception as e:
        raise Exception(f"Error in research_health for {plant_name}: {str(e)}")

















def research_season(plant_name: str):
    """Research seasonal growth and farming details of the plant.

    Args:
        plant_name (str): The name of the plant to research.

    Returns:
        Task: The research task instance with seasonal farming insights.
    """
    try:
        agent = WebResearchAgent.initialize_web_research_agent()

        task = Task.create(
            agent=agent,
            context=f"Plant Name: {plant_name}",
            instruction=(
                f"Research the optimal growth conditions for {plant_name}, covering:\n"
                f"- Ideal planting and harvesting seasons.\n"
                f"- Climate, temperature, and humidity requirements.\n"
                f"- Best soil types, nutrients, and fertilizers.\n"
                f"- Farming practices for maximizing yield.\n"
                f"- Alternative uses or storage methods for off-seasons.\n"
                f"Provide reliable agricultural data and expert recommendations."
            ),
        )

        return task

    except Exception as e:
        raise Exception(f"Error in research_season for {plant_name}: {str(e)}")


















def research_price(plant_name: str):
    """Research market price details of the plant.

    Args:
        plant_name (str): The name of the plant to research.

    Returns:
        Task: The research task instance with market pricing insights.
    """
    try:
        agent = PriceFetchingAgent.initialize_price_fetching_agent(query=plant_name)

        task = Task.create(
            agent=agent,
            context=f"Plant Name: {plant_name}",
            instruction=(
                f"Gather market price information for {plant_name}, focusing on:\n"
                f"- Price comparisons across online and offline markets.\n"
                f"- Cost per kilogram vs. per pound for different quality grades.\n"
                f"- Price variations based on country, state, or region (prioritize user location).\n"
                f"- Factors affecting pricing (seasonality, demand, supply, and quality).\n"
                f"Provide accurate, up-to-date data from reliable sources."
            ),
        )

        return task

    except Exception as e:
        raise Exception(f"Error in research_price for {plant_name}: {str(e)}")











# Route for the home page
@app.route("/")
def index():
    return render_template("index.html")

# Route for prediction
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get the image data from the request
        data = request.json["image"]
        image_data = base64.b64decode(data)
        logger.info("Image data received and decoded.")

        # Process the image and get the results
        labels_text, error, processed_image = process_prediction(image_data, "uploaded_image.jpg")
        if error:
            logger.error(f"Error in process_prediction: {error}")
            return jsonify({"error": error, "image": None}), 500

        # Read detected objects from the file
        detected_objects = read_detected_objects(DETECTED_OBJECTS_PATH)
        logger.info(f"Detected objects: {detected_objects}")

        # Initialize research results and summarized report
        research_results = {}
        summarized_report = "No detected objects to generate a report."

        # If objects are detected, perform research and generate a report
        if detected_objects:
            logger.info("Starting research and report generation.")
            try:
                research_results = execute_research_and_report(detected_objects)
                summarized_report = generate_summarized_report(research_results)
                logger.info("Research and report generation completed.")
            except Exception as e:
                logger.error(f"Error in research and report generation: {str(e)}")
                # Continue even if research fails, but return the image and detected objects

        # Return the results as JSON
        return jsonify(
            {
                "labels_text": labels_text,
                "image": processed_image,  # Ensure this is always included
                "detected_objects": detected_objects,
                "research_results": research_results,
                "summarized_report": summarized_report,
            }
        )
    except Exception as e:
        logger.error(f"Error in predict endpoint: {str(e)}")
        return jsonify({"error": str(e), "image": None}), 500

# Route to handle email submission
@app.route("/send-report", methods=["POST"])
def send_report():
    try:
        data = request.json
        email = data.get("email")
        summarized_report = data.get("summarized_report")

        if not email or not summarized_report:
            logger.error("Email or summarized report missing in request.")
            return {"error": "Email and summarized report are required."}, 400

        # Send the email
        subject = "Your Summarized Report from Leaflogic"
        body = f"Here is your summarized report:\n\n{summarized_report}"
        logger.info(f"Sending email to: {email}")

        if send_email(email, subject, body):
            logger.info("Email sent successfully.")
            return {"message": "Report sent successfully!"}, 200
        else:
            logger.error("Failed to send email.")
            return {"error": "Failed to send the report."}, 500
    except Exception as e:
        logger.error(f"Error in send_report endpoint: {str(e)}")
        return {"error": str(e)}, 500
    


    

if __name__ == "__main__":
    app.run(debug=True)






