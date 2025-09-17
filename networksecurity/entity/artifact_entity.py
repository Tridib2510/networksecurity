
# The  Data Ingestion Artifacts inclues all the outputs that we want 
# from Data Ingestion Component
# The output of DataIngestion Component should be the 
# trained_file_path and test_file_path

from dataclasses import dataclass
# dataclass creates variable for an empty class

@dataclass
class DataIngestionArtifact:
    trained_file_path:str
    test_file_path:str

# data validation artifact
@dataclass
class DataValidationArtifact:
    validation_status:bool
    valid_train_file_path:str
    valid_test_file_path:str
    invalid_train_file_path:str
    invalid_test_file_path:str
    drift_report_file_path:str

@dataclass
class DataTransformationArtifact:
    transformed_object_file_path:str
    transformed_train_file_path:str
    transformed_test_file_path:str

@dataclass
class ClassificationMetricArtifact:
    f1_score:float
    precision_score:float
    recall_score:float

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path:str
    train_metric_artifact:ClassificationMetricArtifact
    test_metric_artifact:ClassificationMetricArtifact
