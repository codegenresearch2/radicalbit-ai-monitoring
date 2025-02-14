from .aws_credentials import AwsCredentials
from .column_definition import ColumnDefinition
from .data_type import DataType
from .dataset_data_quality import (
    ClassificationDataQuality,
    CategoricalFeatureMetrics,
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
from .file_upload_result import CurrentFileUpload, FileReference, ReferenceFileUpload
from .job_status import JobStatus
from .model_definition import (
    CreateModel,
    Granularity,
    ModelDefinition,
    OutputType,
)
from .model_type import ModelType
from .supported_types import SupportedTypes

__all__ = [
    'OutputType',
    'Granularity',
    'CreateModel',
    'ModelDefinition',
    'ColumnDefinition',
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
    'FeatureMetrics',
    'NumericalFeatureMetrics',
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
]

# Enhancing ModelDefinition with ModelFeatures
class ModelFeatures(ModelDefinition):
    def update_features(self, new_features: List[ColumnDefinition]):
        self.features = new_features

    def add_feature(self, new_feature: ColumnDefinition):
        self.features.append(new_feature)

    def remove_feature(self, feature_name: str):
        self.features = [feature for feature in self.features if feature.name != feature_name]

# Maintaining consistent naming conventions
class ModelOut(ModelFeatures):
    # rest of the class definition...