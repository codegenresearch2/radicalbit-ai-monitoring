from enum import Enum
from typing import List, Optional
import uuid as uuid_lib

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from spark.jobs.utils.models import ColumnDefinition, DataType, ModelType, Granularity, OutputType

class BaseModelDefinition(BaseModel):
    """A base class for model definition.\n\n    Attributes:\n        name: The name of the model.\n        description: An optional description to explain something about the model.\n        model_type: The type of the model\n        data_type: It explains the data type used by the model\n        granularity: The window used to calculate aggregated metrics\n        features: A list column representing the features set\n        outputs: An OutputType definition to explain the output of the model\n        target: The column used to represent model's target\n        timestamp: The column used to store when prediction was done\n        frameworks: An optional field to describe the frameworks used by the model\n        algorithm: An optional field to explain the algorithm used by the model\n\n    """

    name: str
    description: Optional[str] = None
    model_type: ModelType
    data_type: DataType
    granularity: Granularity
    features: List[ColumnDefinition]
    outputs: OutputType
    target: ColumnDefinition
    timestamp: ColumnDefinition
    frameworks: Optional[str] = None
    algorithm: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )

class CreateModel(BaseModelDefinition):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    def add_feature(self, feature: ColumnDefinition):
        self.features.append(feature)

class ModelDefinition(BaseModelDefinition):
    uuid: uuid_lib.UUID = Field(default_factory=lambda: uuid_lib.uuid4())
    created_at: str = Field(alias='createdAt')
    updated_at: str = Field(alias='updatedAt')

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    def update_features(self, features: List[ColumnDefinition]):
        self.features = features

I have rewritten the code according to the provided rules. I have added a method `add_feature` to the `CreateModel` class to enable adding new model features functionality. I have also added a method `update_features` to the `ModelDefinition` class to enhance model update capabilities with new features. I have maintained code organization by importing necessary components from the `spark.jobs.utils.models` module.