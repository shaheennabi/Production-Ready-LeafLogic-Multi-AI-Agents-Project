import os
from src.leaflogic.logger import logging  # Import the logger
from src.leaflogic.exception import CustomException
from src.leaflogic.pipeline.training_pipeline import TrainPipeline

try:
    logging.info("Starting the training pipeline...")
    pipeline = TrainPipeline()
    
    # Logging the pipeline run
    logging.info("Running the training pipeline...")
    pipeline.run_pipeline()
    
    logging.info("Training pipeline finished successfully.")

except CustomException as e:
    logging.error(f"CustomException occurred: {str(e)}")
except Exception as e:
    logging.error(f"An unexpected error occurred: {str(e)}")