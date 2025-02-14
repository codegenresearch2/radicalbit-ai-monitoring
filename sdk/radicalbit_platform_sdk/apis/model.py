import os
from typing import List, Optional
from uuid import UUID

import boto3
from botocore.exceptions import ClientError as BotoClientError
import pandas as pd
from pydantic import TypeAdapter, ValidationError
import requests

from radicalbit_platform_sdk.apis import ModelCurrentDataset, ModelReferenceDataset
from radicalbit_platform_sdk.commons import invoke
from radicalbit_platform_sdk.errors import ClientError
from radicalbit_platform_sdk.models import (
    AwsCredentials,
    ColumnDefinition,
    CurrentFileUpload,
    DataType,
    FileReference,
    Granularity,
    ModelDefinition,
    ModelType,
    OutputType,
    ReferenceFileUpload,
)

class ModelFeatures:
    def __init__(self, features: List[ColumnDefinition]) -> None:
        self.__features = features

    def features(self) -> List[ColumnDefinition]:
        return self.__features

class Model:
    def __init__(self, base_url: str, definition: ModelDefinition) -> None:
        self.__base_url = base_url
        self.__uuid = definition.uuid
        self.__name = definition.name
        self.__description = definition.description
        self.__model_type = definition.model_type
        self.__data_type = definition.data_type
        self.__granularity = definition.granularity
        self.__features = ModelFeatures(definition.features)
        self.__target = definition.target
        self.__timestamp = definition.timestamp
        self.__outputs = definition.outputs
        self.__frameworks = definition.frameworks
        self.__algorithm = definition.algorithm

    # Rest of the code remains the same