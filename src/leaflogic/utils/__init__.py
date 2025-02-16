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
    

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as file:
            yaml.dump(content, file)
            logging.info("Successfully write_yaml_file")

    except Exception as e:
        raise CustomException(e, sys)
    



def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open("./data/" + fileName, 'wb') as f:
        f.write(imgdata)
        f.close()


def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())