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
from .dataset_drift import Drift, DriftAlgorithm, FeatureDrift, FeatureDriftCalculation
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
from .model_definition import CreateModel, Granularity, ModelDefinition, OutputType
from .model_type import ModelType
from .supported_types import SupportedTypes

class DynamicModelDefinition(ModelDefinition):
    def add_feature(self, feature: ColumnDefinition):
        self.features.append(feature)

    def add_output(self, output: ColumnDefinition):
        self.outputs.output.append(output)

    def add_prediction_proba(self, prediction_proba: ColumnDefinition):
        self.outputs.prediction_proba = prediction_proba

    def add_target(self, target: ColumnDefinition):
        self.target = target

    def add_timestamp(self, timestamp: ColumnDefinition):
        self.timestamp = timestamp

# Example usage
model = DynamicModelDefinition(
    uuid="your-uuid",
    name="your-model-name",
    description="your-model-description",
    model_type=ModelType.REGRESSION,
    data_type=DataType.TABULAR,
    granularity=Granularity.DAY,
    features=[],
    outputs=OutputType(prediction=ColumnDefinition(name="prediction", type=SupportedTypes.float, field_type=FieldType.numerical), output=[]),
    created_at="2022-01-01",
    updated_at="2022-01-02"
)

model.add_feature(ColumnDefinition(name="feature1", type=SupportedTypes.int, field_type=FieldType.numerical))
model.add_output(ColumnDefinition(name="output1", type=SupportedTypes.string, field_type=FieldType.categorical))
model.add_prediction_proba(ColumnDefinition(name="prediction_proba", type=SupportedTypes.float, field_type=FieldType.numerical))
model.add_target(ColumnDefinition(name="target", type=SupportedTypes.float, field_type=FieldType.numerical))
model.add_timestamp(ColumnDefinition(name="timestamp", type=SupportedTypes.datetime, field_type=FieldType.datetime))

# Example API response for testing
response = {
    "uuid": "your-uuid",
    "name": "your-model-name",
    "description": "your-model-description",
    "model_type": "REGRESSION",
    "data_type": "TABULAR",
    "granularity": "DAY",
    "features": [
        {
            "name": "feature1",
            "type": "int",
            "field_type": "numerical"
        }
    ],
    "outputs": {
        "prediction": {
            "name": "prediction",
            "type": "float",
            "field_type": "numerical"
        },
        "prediction_proba": {
            "name": "prediction_proba",
            "type": "float",
            "field_type": "numerical"
        },
        "output": [
            {
                "name": "output1",
                "type": "string",
                "field_type": "categorical"
            }
        ]
    },
    "target": {
        "name": "target",
        "type": "float",
        "field_type": "numerical"
    },
    "timestamp": {
        "name": "timestamp",
        "type": "datetime",
        "field_type": "datetime"
    },
    "created_at": "2022-01-01",
    "updated_at": "2022-01-02"
}