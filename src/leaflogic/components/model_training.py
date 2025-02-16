import os
import sys
import yaml
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
            
            # Validate required files
            if not os.path.exists(self.data_yaml_path):
                raise FileNotFoundError(f"❌ data.yaml not found at {self.data_yaml_path}")
            
            if not os.path.exists(self.model_config_path):
                raise FileNotFoundError(f"❌ Updated model config not found at {self.model_config_path}")
            
            logging.info("✅ ModelTrainer initialized successfully.")
        except Exception as e:
            logging.error(f"❌ Error initializing ModelTrainer: {e}")
            raise CustomException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifacts:
        """
        Starts the YOLOv5 training process.
        """
        try:
            logging.info("🚀 Starting Model Training...")

            # Run YOLOv5 training
            os.system(
                f"cd yolov5 && python train.py --img 416 --batch {self.model_trainer_config.batch_size} "
                f"--epochs {self.model_trainer_config.no_epochs} --data {self.data_yaml_path} "
                f"--cfg {self.model_config_path} --weights {self.model_trainer_config.weight_name} "
                f"--name yolov5_results --cache"
            )

            # Check if training was successful
            best_model_path = "yolov5/runs/train/yolov5_results/weights/best.pt"
            if not os.path.exists(best_model_path):
                raise FileNotFoundError("❌ Best model weights not found after training.")
            
            # Ensure the target directory exists
            os.makedirs(self.model_trainer_dir, exist_ok=True)

            # Save best model weights
            os.system(f"cp {best_model_path} {self.model_trainer_dir}/")
            os.system(f"cp {best_model_path} yolov5/")

            # Cleanup
            os.system("rm -rf yolov5/runs")

            # Create artifact
            model_trainer_artifact = ModelTrainerArtifacts(
                trained_model_file_path=os.path.join(self.model_trainer_dir, "best.pt")
            )
            
            logging.info("🏁 Model Training completed successfully.")
            return model_trainer_artifact

        except Exception as e:
            logging.error(f"❌ Error in Model Training: {e}")
            raise CustomException(e, sys)
