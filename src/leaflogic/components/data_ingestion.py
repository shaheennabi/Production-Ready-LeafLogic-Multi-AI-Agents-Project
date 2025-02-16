import os
import sys
from datetime import datetime
from src.leaflogic.logger import logging
from src.leaflogic.exception import CustomException
from src.leaflogic.entity.config_entity import DataIngestionConfig
from src.leaflogic.entity.artifacts_entity import DataIngestionArtifact
from src.leaflogic.utils import Zipper
from src.leaflogic.configuration.s3_configs import S3FileDownloader


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        """
        Initializes the DataIngestion class with the provided config.
        """
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            logging.error(f"Error initializing DataIngestion: {e}")
            raise CustomException(e, sys)

    def download_data(self) -> str:
        """
        Download the dataset zip file from S3 to the specified data ingestion directory.
        """
        logging.info("Entered download_data method")
        try:
            # Define the data ingestion directory from config
            data_ingestion_dir = self.data_ingestion_config.data_ingestion_dir
            os.makedirs(data_ingestion_dir, exist_ok=True)

            # Define the local path for the downloaded zip file
            zip_file_path = os.path.join(data_ingestion_dir, "leaflogic_dataset.zip")

            # Download the file using S3FileDownloader
            s3_downloader = S3FileDownloader(local_file_path=zip_file_path)
            success = s3_downloader.run()

            if success:
                logging.info(f"✅ Data successfully downloaded to {zip_file_path}")
                return zip_file_path
            else:
                logging.error("❌ Data download failed.")
                raise CustomException("Data download failed.")

        except Exception as e:
            logging.error(f"Exception in download_data: {e}")
            raise CustomException(e, sys)

    def extract_zip_file(self, zip_file_path: str) -> str:
        """
        Extracts the zip file into the feature_store directory.
        """
        logging.info(f"Extracting {zip_file_path} into feature store")
        try:
            # Define the feature store directory
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(feature_store_path, exist_ok=True)

            # Unzip the file
            unzipper = Zipper(zip_file_path=zip_file_path, extract_to_folder=feature_store_path)
            unzipper.unzip()

            logging.info(f"✅ Extraction completed. Files are stored in {feature_store_path}")
            return feature_store_path

        except Exception as e:
            logging.error(f"❌ Error extracting zip file: {e}")
            raise CustomException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Orchestrates the data ingestion process: downloading and extracting the zip file.
        """
        logging.info("Entered initiate_data_ingestion method of DataIngestion class")
        try:
            # Step 1: Download the zip file
            zip_file_path = self.download_data()

            # Step 2: Extract the zip file into the feature store directory
            feature_store_path = self.extract_zip_file(zip_file_path)

            # Step 3: Create a DataIngestionArtifact object to track paths
            data_ingestion_artifact = DataIngestionArtifact(
                data_zip_file_path=zip_file_path,
                feature_store_path=feature_store_path
            )

            logging.info(f"✅ Data ingestion completed successfully: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            logging.error(f"❌ Error in initiate_data_ingestion: {e}")
            raise CustomException(e, sys)
