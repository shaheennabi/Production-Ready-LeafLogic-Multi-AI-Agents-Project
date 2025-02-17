import os
import sys
import yaml
from src.leaflogic.logger import logging
from src.leaflogic.exception import CustomException
from src.leaflogic.utils import read_yaml_file, write_yaml_file
from src.leaflogic.entity.config_entity import PrepareBaseModelConfig
from src.leaflogic.entity.artifacts_entity import PrepareBaseModelArtifacts, DataIngestionArtifact


class PrepareBaseModel:
    def __init__(self, prepare_base_model_config: PrepareBaseModelConfig, data_ingestion_artifacts: DataIngestionArtifact):
        """
        Initializes PrepareBaseModel class with configuration and data ingestion artifacts.
        """
        try:
            logging.info("🔧 Initializing PrepareBaseModel...")
            self.prepare_base_model_config = prepare_base_model_config
            self.data_ingestion_artifacts = data_ingestion_artifacts

            self.data_yaml_path = os.path.join(self.data_ingestion_artifacts.feature_store_path, "data.yaml")

            if not os.path.exists(self.data_yaml_path):
                raise FileNotFoundError(f"❌ data.yaml not found at: {self.data_yaml_path}")

            logging.info(f"✅ PrepareBaseModel initialized successfully. Using data.yaml: {self.data_yaml_path}")
        except Exception as e:
            logging.error(f"❌ Error in PrepareBaseModel initialization: {e}")
            raise CustomException(e, sys)

    def update_model_config(self) -> str:
        """
        Updates the YOLOv5 model config file by modifying the number of classes (nc).
        Ensures structure remains identical to the base model.
        """
        try:
            logging.info("⚙️ Updating model configuration for custom training...")
            
            data_yaml_content = read_yaml_file(self.data_yaml_path)
            num_classes = data_yaml_content.get("nc")

            if num_classes is None:
                raise ValueError("❌ 'nc' (number of classes) is missing in data.yaml")

            model_config_file_name = os.path.splitext(self.prepare_base_model_config.base_model_name)[0]
            model_config_path = os.path.join("yolov5\models", f"{model_config_file_name}.yaml")

            if not os.path.exists(model_config_path):
                raise FileNotFoundError(f"❌ Base model config file not found at: {model_config_path}")

            config = read_yaml_file(model_config_path)
            config["nc"] = int(num_classes)  # Update class count
            
            # Ensure structure remains identical to the original
            config["anchors"] = config.get("anchors", [])
            config["backbone"] = config.get("backbone", [])
            config["head"] = config.get("head", [])
            config["depth_multiple"] = config.get("depth_multiple", 0.33)
            config["width_multiple"] = config.get("width_multiple", 0.50)
            
            # Save the updated config as a new custom model config
            custom_model_config_path = os.path.join("yolov5\models", f"custom_{model_config_file_name}.yaml")
            write_yaml_file(custom_model_config_path, config)

            logging.info(f"✅ Model config updated and saved at: {custom_model_config_path}")
            return custom_model_config_path

        except Exception as e:
            logging.error(f"❌ Error updating model configuration: {e}")
            raise CustomException(e, sys)

    def prepare_model(self) -> PrepareBaseModelArtifacts:
        """
        Prepares the YOLOv5 base model for training by updating its configuration.
        Ensures structural integrity.
        Returns an artifact containing the updated config file path.
        """
        try:
            logging.info("🚀 Preparing the base model...")
            custom_model_config_path = self.update_model_config()

            prepare_base_model_artifact = PrepareBaseModelArtifacts(
                updated_model_config_path=custom_model_config_path
            )

            logging.info(f"🏁 Base model preparation completed successfully: {prepare_base_model_artifact}")
            return prepare_base_model_artifact

        except Exception as e:
            logging.error(f"❌ Error in base model preparation: {e}")
            raise CustomException(e, sys)
