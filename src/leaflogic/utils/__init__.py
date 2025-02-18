import sys
from src.leaflogic.exception import CustomException
from src.leaflogic.logger import logging
import zipfile
import os
import os.path
import yaml
import base64
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
    





def decodeImage(image, fileName):
    try:
        imgdata = base64.b64decode(image)
        # Use os.path.join for platform-independent path construction
        full_path = os.path.join("data", fileName)  # Or if data is in parent: os.path.join("..", "data", fileName)
        print(f"Full Path in decodeImage: {full_path}") # Print the path for debugging.
        with open(full_path, 'wb') as f:
            f.write(imgdata)
        logging.info(f"Image successfully decoded and saved at: {full_path}")
    except Exception as e:
        logging.error(f"Error in decodeImage: {str(e)}")
        raise  # Re-raise the exception to be caught in app.py


def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())