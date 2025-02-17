import os
from dataclasses import dataclass
from datetime import datetime
from src.leaflogic.constant import *


TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

@dataclass
class TrainingPipelineConfig:
    artifacts_dir: str = os.path.join(ARTIFACTS_DIR,TIMESTAMP)



training_pipeline_config:TrainingPipelineConfig = TrainingPipelineConfig() 



@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(
        training_pipeline_config.artifacts_dir, DATA_INGESTION_DIR_NAME
    )

    feature_store_file_path: str = os.path.join(
        data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR
    )
    s3_bucket_name = S3_BUCKET_NAME
    s3_data_key = S3_DATA_KEY


@dataclass
class PrepareBaseModelConfig:
    prepare_basemodel_dir: str = os.path.join(
        training_pipeline_config.artifacts_dir, PREPARE_BASEMODEL_DIR_NAME
    )
    base_model_name = PREPARE_BASE_MODEL_NAME


@dataclass
class ModelTrainerConfig: 
    model_trainer_dir: str = os.path.join(training_pipeline_config.artifacts_dir, MODEL_TRAINER_DIR_NAME)

    no_epochs = MODEL_TRAINER_NO_EPOCHS
    
    batch_size = MODEL_TRAINER_BATCH_SIZE

    weight_name = MODEL_TRAINER_WEIGHT_NAME

