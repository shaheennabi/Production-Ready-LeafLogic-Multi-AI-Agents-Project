import os
import boto3
from dotenv import load_dotenv  
from src.leaflogic.logger import logging
from src.leaflogic.exception import CustomException
from boto3.s3.transfer import TransferConfig
import threading

class ProgressPercentage:
    """Class to track download progress."""
    def __init__(self, filename, filesize):
        self._filename = filename
        self._filesize = filesize
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        """Update the progress bar."""
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._filesize) * 100
            logging.info(f"📥 Download progress: {percentage:.2f}% ({self._seen_so_far}/{self._filesize} bytes)")

class S3FileDownloader:
    """Class to download a file (ZIP or any other) from AWS S3."""

    # Default values for bucket, S3 key, and region
    BUCKET_NAME = "leaflogic1"
    S3_KEY = "leaflogic_dataset.zip"
    REGION = "us-east-1"

    def __init__(self, local_file_path):
        # Load environment variables from .env
        load_dotenv()

        self.bucket_name = self.BUCKET_NAME
        self.s3_key = self.S3_KEY
        self.local_file_path = local_file_path
        self.region = self.REGION

        # Get AWS credentials from environment variables
        self.access_key = os.getenv("AWS_ACCESS_KEY")
        self.secret_key = os.getenv("AWS_SECRET_KEY")

        # Validate credentials
        if not self.access_key or not self.secret_key:
            logging.error("AWS credentials not found. Set AWS_ACCESS_KEY and AWS_SECRET_KEY in .env file.")
            raise CustomException("AWS credentials not found. Set AWS_ACCESS_KEY and AWS_SECRET_KEY in .env file.")

        # Initialize S3 client
        try:
            self.s3_client = boto3.client(
                "s3",
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region
            )
            logging.info("✅ Successfully initialized S3 client.")
        except Exception as e:
            logging.error(f"❌ Failed to initialize S3 client: {e}")
            raise CustomException(e)

    def download_file(self):
        """Downloads the file from S3 to a local path with progress logging."""
        try:
            logging.info(f"📥 Starting download: {self.s3_key} from {self.bucket_name} to {self.local_file_path}")

            # Get file size from S3
            file_metadata = self.s3_client.head_object(Bucket=self.bucket_name, Key=self.s3_key)
            file_size = file_metadata["ContentLength"]

            # Download file with progress tracking
            config = TransferConfig(multipart_threshold=5 * 1024 * 1024)  # 5MB parts
            self.s3_client.download_file(
                self.bucket_name,
                self.s3_key,
                self.local_file_path,
                Config=config,
                Callback=ProgressPercentage(self.local_file_path, file_size)
            )

            logging.info("✅ Download successful.")
            return True

        except Exception as e:
            logging.error(f"❌ Error downloading file from S3: {e}")
            raise CustomException(e)

    def run(self):
        """Runs the download process."""
        return self.download_file()
