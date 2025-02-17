import os
import sys
import shutil
from datetime import datetime
from src.leaflogic.logger import logging
from src.leaflogic.exception import CustomException
from src.leaflogic.entity.config_entity import DataIngestionConfig
from src.leaflogic.entity.artifacts_entity import DataIngestionArtifact
from src.leaflogic.utils import Zipper
from src.leaflogic.configuration.s3_configs import S3FileDownloader


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        try:
            logging.info("🔧 Initializing DataIngestion...")
            self.data_ingestion_config = data_ingestion_config
            os.makedirs(self.data_ingestion_config.data_ingestion_dir, exist_ok=True)
            logging.info("✅ DataIngestion initialized successfully.")
        except Exception as e:
            logging.error(f"❌ Error initializing DataIngestion: {e}")
            raise CustomException(e, sys)

    def download_data(self) -> str:
        try:
            logging.info("📥 Starting data download...")
            zip_file_path = os.path.join(self.data_ingestion_config.data_ingestion_dir, "leaflogic_dataset.zip")
            s3_downloader = S3FileDownloader(local_file_path=zip_file_path)
            
            if not s3_downloader.run():
                raise CustomException("❌ Data download failed.")
            
            logging.info(f"✅ Data successfully downloaded to: {zip_file_path}")
            return zip_file_path
        except Exception as e:
            logging.error(f"❌ Error in download_data: {e}")
            raise CustomException(e, sys)

    def extract_zip_file(self, zip_file_path: str) -> str:
        try:
            logging.info(f"📦 Extracting dataset from {zip_file_path}...")
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(feature_store_path, exist_ok=True)
            
            # Extract files into a temporary directory
            temp_extract_path = os.path.join(self.data_ingestion_config.data_ingestion_dir, "temp_extracted")
            os.makedirs(temp_extract_path, exist_ok=True)
            
            unzipper = Zipper(zip_file_path=zip_file_path, extract_to_folder=temp_extract_path)
            unzipper.unzip()
            
            # Move only the contents of leaflogic_dataset to feature_store_path
            extracted_main_folder = os.path.join(temp_extract_path, "leaflogic_dataset")
            if not os.path.exists(extracted_main_folder):
                raise FileNotFoundError("❌ Extracted dataset folder not found: leaflogic_dataset")
            
            for item in os.listdir(extracted_main_folder):
                src_path = os.path.join(extracted_main_folder, item)
                dest_path = os.path.join(feature_store_path, item)
                
                if os.path.isdir(src_path):
                    shutil.move(src_path, feature_store_path)  # Move directories
                else:
                    shutil.move(src_path, dest_path)  # Move files
            
            shutil.rmtree(temp_extract_path)  # Clean up temp extraction folder
            logging.info(f"✅ Extraction completed. Files stored in: {feature_store_path}")
            return feature_store_path
        except Exception as e:
            logging.error(f"❌ Error extracting zip file: {e}")
            raise CustomException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("🚀 Initiating data ingestion...")
            zip_file_path = self.download_data()
            feature_store_path = self.extract_zip_file(zip_file_path)
            
            data_ingestion_artifact = DataIngestionArtifact(
                data_zip_file_path=zip_file_path,
                feature_store_path=feature_store_path
            )
            
            logging.info(f"🏁 Data ingestion completed successfully: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            logging.error(f"❌ Error in initiate_data_ingestion: {e}")
            raise CustomException(e, sys)
