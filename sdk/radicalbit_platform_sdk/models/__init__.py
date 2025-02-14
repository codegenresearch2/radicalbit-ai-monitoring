from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, TypeAdapter
from pyspark.sql.types import StringType, DoubleType, IntegerType, TimestampType

from .aws_credentials import AwsCredentials
from .column_definition import ColumnDefinition
from .data_type import DataType
from .dataset_data_quality import (
    ClassificationDataQuality,
    CategoricalFeatureMetrics,
    RegressionDataQuality,
)
from .dataset_drift import DriftAlgorithm
from .dataset_model_quality import (
    BinaryClassificationModelQuality,
    CurrentBinaryClassificationModelQuality,
    CurrentMultiClassificationModelQuality,
    CurrentRegressionModelQuality,
    MultiClassificationModelQuality,
    RegressionModelQuality,
)
from .dataset_stats import DatasetStats
from .file_upload_result import ReferenceFileUpload, CurrentFileUpload, FileReference
from .job_status import JobStatus
from .model_definition import CreateModel, Granularity, ModelType, OutputType
from .supported_types import SupportedTypes

class ModelFeatures(BaseModel):
    numerical: List[ColumnDefinition]
    float_features: List[ColumnDefinition]
    int_features: List[ColumnDefinition]
    categorical: List[ColumnDefinition]
    datetime: List[ColumnDefinition]

    @classmethod
    def from_model_definition(cls, model_definition: 'ModelDefinition'):
        return cls(
            numerical=model_definition.get_numerical_features(),
            float_features=model_definition.get_float_features(),
            int_features=model_definition.get_int_features(),
            categorical=model_definition.get_categorical_features(),
            datetime=[feature for feature in model_definition.features if feature.is_datetime()],
        )

    def update_features(self, features: List[ColumnDefinition]):
        self.numerical = [feature for feature in features if feature.is_numerical()]
        self.float_features = [feature for feature in features if feature.is_float()]
        self.int_features = [feature for feature in features if feature.is_int()]
        self.categorical = [feature for feature in features if feature.is_categorical()]
        self.datetime = [feature for feature in features if feature.is_datetime()]

class ModelDefinition(BaseModel):
    uuid: UUID
    name: str
    description: Optional[str]
    model_type: ModelType
    data_type: DataType
    granularity: Granularity
    features: ModelFeatures
    outputs: OutputType
    target: ColumnDefinition
    timestamp: ColumnDefinition
    frameworks: Optional[str]
    algorithm: Optional[str]
    created_at: str
    updated_at: str

    model_config = ConfigDict(json_encoders={UUID: str})

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        value = TypeAdapter(ModelDefinition).validate_python(value)
        return str(value.model_dump_json())

    @staticmethod
    def convert_types(t: str):
        match t:
            case SupportedTypes.string:
                return StringType()
            case SupportedTypes.float:
                return DoubleType()
            case SupportedTypes.int:
                return IntegerType()
            case SupportedTypes.bool:
                return StringType()
            case SupportedTypes.datetime:
                return TimestampType()

__all__ = [
    'OutputType',
    'Granularity',
    'CreateModel',
    'ModelDefinition',
    'ModelFeatures',
    'ColumnDefinition',
    'JobStatus',
    'DataType',
    'ModelType',
    'DatasetStats',
    'BinaryClassificationModelQuality',
    'CurrentBinaryClassificationModelQuality',
    'CurrentMultiClassificationModelQuality',
    'MultiClassificationModelQuality',
    'RegressionModelQuality',
    'CurrentRegressionModelQuality',
    'ClassificationDataQuality',
    'RegressionDataQuality',
    'CategoricalFeatureMetrics',
    'DriftAlgorithm',
    'ReferenceFileUpload',
    'CurrentFileUpload',
    'FileReference',
    'AwsCredentials',
    'SupportedTypes',
]