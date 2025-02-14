from enum import Enum
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel
from pyspark.sql.types import (
    StringType,
    DoubleType,
    IntegerType,
    TimestampType,
)

# Enhancing model definition with ModelFeatures
class ModelFeatures(BaseModel):
    uuid: UUID
    name: str
    description: Optional[str]
    type: str
    field_type: str

    def update_feature(self, name: Optional[str] = None, type: Optional[str] = None, field_type: Optional[str] = None):
        if name:
            self.name = name
        if type:
            self.type = type
        if field_type:
            self.field_type = field_type

class ModelDefinition(BaseModel):
    uuid: UUID
    name: str
    description: Optional[str]
    model_type: ModelType
    data_type: DataType
    granularity: Granularity
    features: List[ModelFeatures]
    outputs: OutputType
    target: ModelFeatures
    timestamp: ModelFeatures
    frameworks: Optional[str]
    algorithm: Optional[str]
    created_at: str
    updated_at: str

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

    def get_numerical_features(self) -> List[ModelFeatures]:
        return [feature for feature in self.features if feature.field_type == FieldTypes.numerical]

    def get_float_features(self) -> List[ModelFeatures]:
        return [feature for feature in self.features if feature.field_type == FieldTypes.numerical and feature.type == SupportedTypes.float]

    def get_int_features(self) -> List[ModelFeatures]:
        return [feature for feature in self.features if feature.field_type == FieldTypes.numerical and feature.type == SupportedTypes.int]

    def get_categorical_features(self) -> List[ModelFeatures]:
        return [feature for feature in self.features if feature.field_type == FieldTypes.categorical]

# Maintaining consistent naming conventions in code.
from .aws_credentials import AwsCredentials
from .column_definition import ColumnDefinition
from .data_type import DataType
from .dataset_data_quality import (
    ClassificationDataQuality,
    CategoricalFeatureMetrics,
    CategoryFrequency,
    ClassMedianMetrics,
    ClassMetrics,
    DataQuality,
    FeatureMetrics,
    MedianMetrics,
    MissingValue,
    NumericalFeatureMetrics,
    RegressionDataQuality,
)
from .dataset_drift import (
    Drift,
    DriftAlgorithm,
    FeatureDrift,
    FeatureDriftCalculation,
)
from .dataset_model_quality import (
    BinaryClassificationModelQuality,
    CurrentBinaryClassificationModelQuality,
    CurrentMultiClassificationModelQuality,
    CurrentRegressionModelQuality,
    ModelQuality,
    MultiClassificationModelQuality,
    RegressionModelQuality,
)
from .dataset_stats import DatasetStats
from .field_type import FieldType
from .file_upload_result import CurrentFileUpload, FileReference, ReferenceFileUpload
from .job_status import JobStatus
from .model_definition import (
    CreateModel,
    Granularity,
    OutputType,
)
from .model_type import ModelType
from .supported_types import SupportedTypes

__all__ = [
    'OutputType',
    'Granularity',
    'CreateModel',
    'ModelDefinition',
    'ModelFeatures',
    'JobStatus',
    'DataType',
    'ModelType',
    'DatasetStats',
    'ModelQuality',
    'BinaryClassificationModelQuality',
    'CurrentBinaryClassificationModelQuality',
    'CurrentMultiClassificationModelQuality',
    'MultiClassificationModelQuality',
    'RegressionModelQuality',
    'CurrentRegressionModelQuality',
    'DataQuality',
    'ClassificationDataQuality',
    'RegressionDataQuality',
    'ClassMetrics',
    'MedianMetrics',
    'MissingValue',
    'ClassMedianMetrics',
    'FeatureMetrics',
    'NumericalFeatureMetrics',
    'CategoryFrequency',
    'CategoricalFeatureMetrics',
    'DriftAlgorithm',
    'FeatureDriftCalculation',
    'FeatureDrift',
    'Drift',
    'ReferenceFileUpload',
    'CurrentFileUpload',
    'FileReference',
    'AwsCredentials',
    'SupportedTypes',
    'FieldType',
]