import sys
import os

from src.leaflogic.components.data_ingestion import DataIngestion
from src.leaflogic.logger import logging
from src.leaflogic.exception import CustomException
from src.leaflogic.entity.config_entity import DataIngestionConfig, PrepareBaseModelConfig, ModelTrainerConfig
from src.leaflogic.entity.artifacts_entity import DataIngestionArtifact, PrepareBaseModelArtifacts, ModelTrainerArtifacts
from src.leaflogic.components.prepare_base_model import PrepareBaseModel
from src.leaflogic.components.model_training import ModelTrainer


class TrainPipeline:
    """Class to orchestrate the entire training pipeline."""

    def __init__(self) -> None:
        try:
            logging.info("🔧 Initializing TrainPipeline...")

            # Initialize configurations
            self.data_ingestion_config = DataIngestionConfig()
            self.prepare_base_model_config = PrepareBaseModelConfig()
            self.model_trainer_config = ModelTrainerConfig()

            logging.info("✅ TrainPipeline initialized successfully.")

        except Exception as e:
            logging.error(f"❌ Error during TrainPipeline initialization: {e}")
            raise CustomException(e, sys)

    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        Starts the data ingestion process and returns the ingestion artifact.
        """
        try:
            logging.info("📥 Starting Data Ingestion process...")

            # Initialize Data Ingestion component
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)

            # Run the ingestion process
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info(f"✅ Data Ingestion completed successfully. Artifact: {data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            logging.error(f"❌ Error in Data Ingestion: {e}")
            raise CustomException(e, sys)

    def start_prepare_base_model(self, data_ingestion_artifact: DataIngestionArtifact) -> PrepareBaseModelArtifacts:
        """
        Prepares the YOLOv5 model by updating its configuration.
        """
        try:
            logging.info("⚙️ Starting Prepare Base Model process...")

            # Initialize Prepare Base Model component
            prepare_base_model = PrepareBaseModel(
                prepare_base_model_config=self.prepare_base_model_config,
                data_ingestion_artifacts=data_ingestion_artifact
            )

            # Prepare the model and return artifacts
            prepare_base_model_artifact = prepare_base_model.prepare_model()

            logging.info(f"✅ Prepare Base Model completed successfully. Artifact: {prepare_base_model_artifact}")

            return prepare_base_model_artifact

        except Exception as e:
            logging.error(f"❌ Error in Prepare Base Model: {e}")
            raise CustomException(e, sys)

    def start_model_training(self, prepare_base_model_artifact: PrepareBaseModelArtifacts, data_ingestion_artifact: DataIngestionArtifact) -> ModelTrainerArtifacts:
        """
        Starts the model training process using YOLOv5.
        """
        try:
            logging.info("🎯 Starting Model Training...")

            # Initialize Model Trainer component
            model_trainer = ModelTrainer(
                model_trainer_config=self.model_trainer_config,
                prepare_base_model_artifacts=prepare_base_model_artifact,
                data_ingestion_artifact=data_ingestion_artifact
            )

            # Train the model and return artifacts
            model_trainer_artifact = model_trainer.initiate_model_trainer()

            logging.info(f"✅ Model Training completed successfully. Artifact: {model_trainer_artifact}")

            return model_trainer_artifact

        except Exception as e:
            logging.error(f"❌ Error in Model Training: {e}")
            raise CustomException(e, sys)

    def run_pipeline(self) -> None:
        """
        Executes the complete ML pipeline.
        """
        try:
            logging.info("🚀 Starting the Training Pipeline...")

            # Step 1: Data Ingestion
            data_ingestion_artifact = self.start_data_ingestion()

            # Step 2: Prepare Base Model
            prepare_base_model_artifact = self.start_prepare_base_model(data_ingestion_artifact)

            # Step 3: Model Training
            model_trainer_artifact = self.start_model_training(prepare_base_model_artifact, data_ingestion_artifact)

            logging.info(f"🏁 Training Pipeline executed successfully! Final Model Path: {model_trainer_artifact.trained_model_file_path}")

        except Exception as e:
            logging.error(f"❌ Training Pipeline failed: {e}")
            raise CustomException(e, sys)


# Run the pipeline when script is executed
if __name__ == "__main__":
    pipeline = TrainPipeline()
    pipeline.run_pipeline()
