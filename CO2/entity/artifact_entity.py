from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    feature_store_file_path: str


@dataclass
class DataValidationArtifact:
    report_file_path: str


@dataclass
class DataTransformationArtifact:
    transform_object_path:str
    transformed_train_object:str
    transformed_test_object:str


class ModelTrainerArtifact: ...


class ModelEvaluationArtifact: ...


class ModelPusherArtifact: ...