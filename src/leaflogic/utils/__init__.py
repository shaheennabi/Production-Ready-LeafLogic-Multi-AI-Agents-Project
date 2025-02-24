import sys
from src.leaflogic.exception import CustomException
from src.leaflogic.logger import logging
import zipfile
import os
import os.path
import yaml
import base64
import re
from taskflowai import OpenaiModels, set_verbosity
from dotenv import load_dotenv
from PIL import Image
import io



class Zipper:
    
    def __init__(self, zip_file_path, extract_to_folder):
        self.zip_file_path = zip_file_path
        self.extract_to_folder = extract_to_folder

    try:
        def unzip(self):
            with zipfile.ZipFile(self.zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(self.extract_to_folder)
    

    except Exception as e:
        raise CustomException(e, sys)
    






def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            logging.info("Read yaml file successfully")
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise CustomException(e, sys) from e
    

## written by anthropic claude for me (sonnet 3.5), it was too difficult to code this...
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    """
    Write YAML file in YOLOv5 format with specific styling.
    """
    try:
        if replace and os.path.exists(file_path):
            os.remove(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Open file with UTF-8 encoding to handle emojis and special characters
        with open(file_path, "w", encoding='utf-8') as file:
            # Write header without emoji to avoid encoding issues
            file.write("# Ultralytics AGPL-3.0 License - https://ultralytics.com/license\n\n")
            file.write("# Parameters\n")
            
            # Write base parameters with comments
            file.write(f"nc: {content['nc']} # number of classes\n")
            file.write(f"depth_multiple: {content['depth_multiple']} # model depth multiple\n")
            file.write(f"width_multiple: {content['width_multiple']} # layer channel multiple\n")
            
            # Write anchors with comments
            file.write("anchors:\n")
            file.write(f"  - {content['anchors'][0]} # P3/8\n")
            file.write(f"  - {content['anchors'][1]} # P4/16\n")
            file.write(f"  - {content['anchors'][2]} # P5/32\n\n")
            
            # Write backbone
            file.write("# YOLOv5 v6.0 backbone\n")
            file.write("backbone:\n")
            file.write("  # [from, number, module, args]\n")
            file.write("  [\n")
            
            # Define backbone comments
            backbone_comments = {
                0: "0-P1/2",
                1: "1-P2/4",
                3: "3-P3/8",
                5: "5-P4/16",
                7: "7-P5/32",
                9: "9"
            }
            
            # Write backbone layers
            for i, layer in enumerate(content['backbone']):
                comment = f" # {backbone_comments[i]}" if i in backbone_comments else ""
                file.write(f"    {layer},{comment}\n")
            file.write("  ]\n\n")
            
            # Write head
            file.write("# YOLOv5 v6.0 head\n")
            file.write("head: [\n")
            
            # Define head comments
            head_comments = {
                2: "cat backbone P4",
                3: "13",
                6: "cat backbone P3",
                7: "17 (P3/8-small)",
                9: "cat head P4",
                10: "20 (P4/16-medium)",
                12: "cat head P5",
                13: "23 (P5/32-large)",
                14: "Detect(P3, P4, P5)"
            }
            
            # Write head layers
            for i, layer in enumerate(content['head']):
                comment = f" # {head_comments[i]}" if i in head_comments else ""
                # Add extra newline before certain layers for readability
                if i in [4, 8, 11, 14]:
                    file.write("\n")
                file.write(f"    {layer},{comment}\n")
            file.write("  ]\n")

            logging.info(f"✅ Successfully wrote YAML file at {file_path}")

    except Exception as e:
        logging.error(f"❌ Error writing YAML file: {e}")
        raise CustomException(e, sys)
    







def decodeImage(base64_string, filename):
    try:
        imgdata = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(imgdata))
        file_path = os.path.join("data", filename)
        if not os.path.exists("data"):
            os.makedirs("data")
        image.save(file_path)
        return file_path
    except Exception as e:
        print(f"Error decoding image: {e}")
        return None

def encodeImageIntoBase64(filepath):
    try:
        with open(filepath, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_string
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None
    


labels = [
    'Zingiber officinale -ginger-', 'almonds', 'aloe vera', 'apple fruit', 'apricot', 'areca nut', 'ashwagandha', 'avacado', 'bamboo', 'banana',
    'beetroot', 'bell pepper -capsicum-', 'bitter gourd', 'black pepper', 'blackberry fruit', 'blackgram', 'blueberry fruit', 'bottle gourd', 'brinjal', 'brocoli',
    'cabbage', 'cactus', 'cardamom', 'carrot', 'cashew', 'cassava', 'cauliflower', 'chamomile', 'cherry', 'chilli pepper', 'cinnamon', 'coconut', 'coffee beans', 'coriander', 'cotton', 'cucumber', 'date palm', 'dates', 'dragon fruit', 'figs -anjeer-',
    'garlic', 'grapes', 'green gram -mung bean-', 'groundnut-peanut-', 'guava', 'jaggery', 'jute', 'kidney bean', 'kiwi fruit', 'lavender plant',
    'lemon', 'lychee', 'maize', 'mango', 'mint herb', 'mushroom', 'muskmelon', 'mustard crop', 'oats', 'okra -ladyfinger-', 'onion',
    'orange', 'orchid orchidaceae', 'papaya', 'pea', 'peach', 'pear fruit', 'pineapple', 'pista -pistachio-', 'plum fruit', 'pomegranate',
    'pomelo', 'potato', 'pumpkin', 'radish', 'raspberry fruit', 'rice', 'rose', 'rosemary', 'rubber plant', 'safflower',
    'saffron', 'sesame', 'sorghum', 'soursop', 'soybean', 'spinach', 'starfruit -carambola-', 'strawberry', 'sugar apple', 'sugarcane',
    'sunflower', 'sweet potato', 'tea', 'tomato', 'tulip', 'turmeric', 'walnut', 'watermelon', 'wheat'
]

def get_label_by_index(index):
    if 0 <= index < len(labels):
        return labels[index]
    return "Unknown"



"""GenAI implementation related  from now on"""


# ✅ Load environment variables from .env file
load_dotenv()

# ✅ Set verbosity for taskflowai
set_verbosity(True)

# ✅ Fetch API Keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ Ensure API keys are only checked when they are actually needed
def validate_api_keys():
    """Validates API keys before usage."""
    missing_keys = []
    if not OPENAI_API_KEY:
        missing_keys.append("OPENAI_API_KEY")
    

    if missing_keys:
        raise RuntimeError(f"❌ Missing environment variables: {', '.join(missing_keys)}. Set them in the .env file.")

class LoadModel:
    @staticmethod
    def load_openai_model():
        """
        Load and return the OpenAI GPT-3.5-turbo model.
        This will validate API keys only when called.
        """
        try:
            validate_api_keys()  # Only check when this function is called
            logging.info("Loading OpenAI GPT-3.5-turbo model.")
            model = OpenaiModels.gpt_3_5_turbo
            logging.info("✅ OpenAI GPT-3.5-turbo model loaded successfully.")
            return model
        except Exception as e:
            logging.error("❌ Failed to load OpenAI GPT-3.5-turbo model.")
            raise RuntimeError(f"Error loading OpenAI model: {e}") from e








