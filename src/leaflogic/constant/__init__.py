import os

ARTIFACTS_DIR: str = "artifacts"


"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_DIR_NAME: str = "data_ingestion"

DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"

S3_BUCKET_NAME: str = "leaflogic1"

S3_DATA_KEY: str = "leaflogic_dataset.zip"

"""
Prepare BaseModel related constant  here
"""

PREPARE_BASEMODEL_DIR_NAME: str = "prepare_basemodel"

PREPARE_BASE_MODEL_NAME: str = "yolov5s.pt"


"""  
Model Trainer related constant
"""

MODEL_TRAINER_DIR_NAME: str = "model_trainer"

MODEL_TRAINER_NO_EPOCHS: int = 1

MODEL_TRAINER_BATCH_SIZE: int = 16  

MODEL_TRAINER_WEIGHT_NAME: str = "yolov5s.pt"   




