from enum import Enum
from typing import List, Optional
import uuid as uuid_lib

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from radicalbit_platform_sdk.models.column_definition import ColumnDefinition
from radicalbit_platform_sdk.models.data_type import DataType
from radicalbit_platform_sdk.models.model_type import ModelType
from spark.jobs.utils.models import SupportedTypes, FieldTypes

class ModelOutput(BaseModel):
    prediction: ColumnDefinition
    prediction_proba: Optional[ColumnDefinition] = None
    output: List[ColumnDefinition]

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

class Granularity(str, Enum):
    HOUR = 'HOUR'
    DAY = 'DAY'
    WEEK = 'WEEK'
    MONTH = 'MONTH'

class BaseModelDefinition(BaseModel):
    name: str
    description: Optional[str] = None
    model_type: ModelType
    data_type: DataType
    granularity: Granularity
    features: List[ColumnDefinition]
    outputs: ModelOutput
    target: ColumnDefinition
    timestamp: ColumnDefinition
    frameworks: Optional[str] = None
    algorithm: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    def add_feature(self, name: str, type: SupportedTypes, field_type: FieldTypes) -> None:
        self.features.append(ColumnDefinition(name=name, type=type, field_type=field_type))

    def remove_feature(self, name: str) -> None:
        self.features = [feature for feature in self.features if feature.name != name]

class CreateModel(BaseModelDefinition):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

class ModelDefinition(BaseModelDefinition):
    uuid: uuid_lib.UUID = Field(default_factory=lambda: uuid_lib.uuid4())
    created_at: str = Field(alias='createdAt')
    updated_at: str = Field(alias='updatedAt')

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


I have rewritten the code according to the provided rules. I added a method to the `BaseModelDefinition` class to manage model features, allowing for the addition or removal of features. I also renamed the `OutputType` class to `ModelOutput` to maintain consistent naming conventions and improve code readability.