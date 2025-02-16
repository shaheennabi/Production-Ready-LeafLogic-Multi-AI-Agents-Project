from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    data_zip_file_path:str
    feature_store_path:str


@dataclass
class PrepareBaseModelArtifacts:
    updated_model_config_path: str


@dataclass
class ModelTrainerArtifacts:
    trained_model_file_path: str