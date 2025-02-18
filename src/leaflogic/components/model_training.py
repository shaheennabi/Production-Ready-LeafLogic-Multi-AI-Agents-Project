import os
import sys
import shutil
from src.leaflogic.logger import logging
from src.leaflogic.exception import CustomException
from src.leaflogic.entity.config_entity import ModelTrainerConfig
from src.leaflogic.entity.artifacts_entity import ModelTrainerArtifacts, PrepareBaseModelArtifacts, DataIngestionArtifact


class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
        prepare_base_model_artifacts: PrepareBaseModelArtifacts,
        data_ingestion_artifact: DataIngestionArtifact
    ):
        """
        Initializes ModelTrainer with the required artifacts and configurations.
        """
        try:
            logging.info("🔧 Initializing ModelTrainer...")

            self.model_trainer_config = model_trainer_config
            self.prepare_base_model_artifacts = prepare_base_model_artifacts
            self.data_ingestion_artifact = data_ingestion_artifact
            
            # Construct file paths correctly
            self.data_yaml_path = os.path.join(self.data_ingestion_artifact.feature_store_path, "data.yaml")
            self.model_config_path = self.prepare_base_model_artifacts.updated_model_config_path
            self.model_trainer_dir = self.model_trainer_config.model_trainer_dir

            # Log the paths being used for debugging
            logging.info(f"Data YAML Path: {self.data_yaml_path}")
            logging.info(f"Model Config Path: {self.model_config_path}")
            logging.info(f"Model Trainer Directory: {self.model_trainer_dir}")
            
            # Validate required files
            if not os.path.exists(self.data_yaml_path):
                logging.error(f"❌ data.yaml not found at {self.data_yaml_path}")
                raise FileNotFoundError(f"❌ data.yaml not found at {self.data_yaml_path}")
            else:
                logging.info(f"✅ Found data.yaml at {self.data_yaml_path}")
            
            if not os.path.exists(self.model_config_path):
                logging.error(f"❌ Model config not found at {self.model_config_path}")
                raise FileNotFoundError(f"❌ Updated model config not found at {self.model_config_path}")
            else:
                logging.info(f"✅ Found model config at {self.model_config_path}")
            
            logging.info("✅ ModelTrainer initialized successfully.")
        except Exception as e:
            logging.error(f"❌ Error initializing ModelTrainer: {e}")
            raise CustomException(e, sys)

    def move_data_files_to_root(self):
        """
        Moves the necessary files (data.yaml, train, test, valid) to the root directory.
        """
        try:
            # Move data.yaml
            logging.info("📦 Moving data.yaml to root directory...")
            if os.path.exists(self.data_yaml_path):
                shutil.copy(self.data_yaml_path, os.path.join(os.getcwd(), "data.yaml"))
                logging.info("✅ Moved data.yaml to root directory.")
            else:
                logging.error("❌ data.yaml not found in feature store.")
                raise FileNotFoundError("❌ data.yaml not found in feature store.")

            # Move train, test, valid directories
            directories = ['train', 'valid', 'test']
            for directory in directories:
                source_dir = os.path.join(self.data_ingestion_artifact.feature_store_path, directory)
                if os.path.exists(source_dir):
                    shutil.copytree(source_dir, os.path.join(os.getcwd(), directory))
                    logging.info(f"✅ Moved {directory} directory to root.")
                else:
                    logging.error(f"❌ {directory} directory not found in feature store.")
                    raise FileNotFoundError(f"❌ {directory} directory not found in feature store.")
        
        except Exception as e:
            logging.error(f"❌ Error in moving data files: {e}")
            raise CustomException(e, sys)

    def delete_data_files_from_root(self):
        """
        Deletes the data files (data.yaml, train, test, valid) from the root directory after training.
        """
        try:
            # Delete data.yaml, train, test, and valid directories from the root
            if os.path.exists("data.yaml"):
                os.remove("data.yaml")
                logging.info("✅ Deleted data.yaml from root directory.")
            
            directories = ['train', 'valid', 'test']
            for directory in directories:
                if os.path.exists(directory):
                    shutil.rmtree(directory)
                    logging.info(f"✅ Deleted {directory} directory from root.")
        
        except Exception as e:
            logging.error(f"❌ Error in deleting data files from root: {e}")
            raise CustomException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifacts:
        """
        Starts the YOLOv5 training process.
        """
        try:
            # Move the necessary data files to the root directory
            self.move_data_files_to_root()

            logging.info("🚀 Starting Model Training...")

            # Get absolute paths to avoid issues with relative paths in the shell command
            yolov5_path = os.path.join(os.getcwd(), "yolov5")

            # Log paths to help debug
            logging.info(f"YOLOv5 Path: {yolov5_path}")

            # Run YOLOv5 training (use absolute paths and add --device cpu to force CPU usage)
            training_command = (
                f"python {os.path.join(yolov5_path, 'train.py')} --img 416 --batch {self.model_trainer_config.batch_size} "
                f"--epochs {self.model_trainer_config.no_epochs} --data {os.path.join(os.getcwd(), 'data.yaml')} "
                f"--cfg {self.model_config_path} --weights {self.model_trainer_config.weight_name} "
                f"--name yolov5_results --cache --device cpu"
            )

            logging.info(f"Running training command: {training_command}")

            # Execute the training command
            os.system(training_command)

            # Check if training was successful
            best_model_path = os.path.join(os.getcwd(), "yolov5", "runs", "train", "yolov5_results", "weights", "best.pt")
            if not os.path.exists(best_model_path):
                logging.error(f"❌ Best model weights not found after training at {best_model_path}")
                raise FileNotFoundError("❌ Best model weights not found after training.")

            # Move the best model to the current working directory
            target_path = os.path.join(os.getcwd(), "best.pt")
            shutil.copy(best_model_path, target_path)
            logging.info(f"✅ Best model saved to current working directory: {target_path}")

            # Cleanup the 'runs' folder after training is done
            shutil.rmtree(os.path.join(os.getcwd(), "yolov5", "runs"), ignore_errors=True)

            # Delete the data files from the root directory after training
            self.delete_data_files_from_root()

            # Create artifact with the path to the model in current working directory
            model_trainer_artifact = ModelTrainerArtifacts(
                trained_model_file_path=target_path
            )
            
            logging.info("🏁 Model Training completed successfully.")
            return model_trainer_artifact

        except Exception as e:
            logging.error(f"❌ Error in Model Training: {e}")
            raise CustomException(e, sys)