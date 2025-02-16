import sys
import os

from src.leaflogic.components.data_ingestion import DataIngestion
from src.leaflogic.logger import logging
from src.leaflogic.exception import CustomException
from src.leaflogic.entity.config_entity import DataIngestionConfig
from src.leaflogic.entity.artifacts_entity import DataIngestionArtifact


class TrainPipeline:
    """Class to orchestrate the entire training pipeline."""

    def __init__(self) -> None:
        try:
            logging.info("🔧 Initializing TrainPipeline...")

            # Initialize configurations
            self.data_ingestion_config = DataIngestionConfig()

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

    def run_pipeline(self) -> None:
        """
        Executes the complete ML pipeline.
        """
        try:
            logging.info("🚀 Starting the Training Pipeline...")

            # Step 1: Data Ingestion
            data_ingestion_artifact = self.start_data_ingestion()

            # Future Steps: Data Validation, Model Training, Model Evaluation, Model Deployment
            # Example:
            # self.start_data_validation(data_ingestion_artifact)
            # self.start_model_training(data_ingestion_artifact)

            logging.info("🏁 Training Pipeline executed successfully!")

        except Exception as e:
            logging.error(f"❌ Training Pipeline failed: {e}")
            raise CustomException(e, sys)


# Run the pipeline when script is executed
if __name__ == "__main__":
    pipeline = TrainPipeline()
    pipeline.run_pipeline()
