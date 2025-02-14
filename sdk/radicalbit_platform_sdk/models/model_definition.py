from enum import Enum
from typing import List, Optional
import uuid as uuid_lib
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter
from radicalbit_platform_sdk.models.column_definition import ColumnDefinition
from radicalbit_platform_sdk.models.data_type import DataType
from radicalbit_platform_sdk.models.model_type import ModelType

class ModelFeatures(BaseModel):
    features: List[ColumnDefinition] = TypeAdapter(List[ColumnDefinition]).validate_python

class OutputType(BaseModel):
    prediction: ColumnDefinition
    prediction_proba: Optional[ColumnDefinition] = None
    output: List[ColumnDefinition]

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

class Granularity(str, Enum):
    HOUR = 'HOUR'
    DAY = 'DAY'
    WEEK = 'WEEK'
    MONTH = 'MONTH'

class BaseModelDefinition(BaseModel, ModelFeatures):
    name: str
    description: Optional[str] = None
    model_type: ModelType
    data_type: DataType
    granularity: Granularity
    outputs: OutputType
    target: ColumnDefinition
    timestamp: ColumnDefinition
    frameworks: Optional[str] = None
    algorithm: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())

class CreateModel(BaseModelDefinition):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

class ModelDefinition(BaseModelDefinition):
    uuid: uuid_lib.UUID = Field(default_factory=lambda: uuid_lib.uuid4())
    created_at: str = Field(alias='createdAt')
    updated_at: str = Field(alias='updatedAt')

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

# Test for feature update
def test_feature_update():
    model = ModelDefinition(
        name='Test Model',
        model_type=ModelType.REGRESSION,
        data_type=DataType.TABULAR,
        granularity=Granularity.DAY,
        features=[ColumnDefinition(name='feature1', type='string', field_type='categorical')],
        outputs=OutputType(prediction=ColumnDefinition(name='prediction', type='float', field_type='numerical')),
        target=ColumnDefinition(name='target', type='float', field_type='numerical'),
        timestamp=ColumnDefinition(name='timestamp', type='datetime', field_type='datetime')
    )
    assert len(model.features) == 1
    model.features.append(ColumnDefinition(name='feature2', type='int', field_type='numerical'))
    assert len(model.features) == 2