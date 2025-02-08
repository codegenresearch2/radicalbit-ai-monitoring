import os
import time
import unittest
import uuid
import boto3
from moto import mock_aws, mock_s3
import pytest
import responses
from radicalbit_platform_sdk.apis import Model
from radicalbit_platform_sdk.errors import ClientError
from radicalbit_platform_sdk.models import (
    ColumnDefinition,
    DataType,
    FieldType,
    Granularity,
    JobStatus,
    ModelDefinition,
    ModelType,
    OutputType,
    ReferenceFileUpload,
    SupportedTypes,
)


class ModelTest(unittest.TestCase):
    @mock_s3
    @responses.activate
    def test_load_reference_dataset_without_object_name(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        bucket_name = 'test-bucket'
        file_name = 'test.txt'
        column_def = ColumnDefinition(
            name='prediction',
            type=SupportedTypes.float,
            field_type=FieldType.numerical
        )
        expected_path = f's3://{bucket_name}/{model_id}/reference/{file_name}'
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket=bucket_name)
        model = Model(
            base_url,
            ModelDefinition(
                uuid=model_id,
                name='My Model',
                model_type=ModelType.BINARY,
                data_type=DataType.TABULAR,
                granularity=Granularity.DAY,
                outputs=OutputType(prediction=column_def, output=[column_def]),
                target=ColumnDefinition(
                    name='adult',
                    type=SupportedTypes.bool,
                    field_type=FieldType.categorical,
                ),
                timestamp=ColumnDefinition(
                    name='created_at',
                    type=SupportedTypes.datetime,
                    field_type=FieldType.datetime,
                ),
                created_at=str(time.time()),
                updated_at=str(time.time()),
            )
        )
        response = ReferenceFileUpload(
            uuid=uuid.uuid4(),
            path=expected_path,
            date='',
            status=JobStatus.IMPORTING,
        )
        responses.add(
            method=responses.POST,
            url=f'{base_url}/api/models/{str(model_id)}/reference/bind',
            body=response.model_dump_json(),
            status=200,
            content_type='application/json',
        )
        response = model.load_reference_dataset(
            'tests_resources/people.csv', bucket_name
        )
        assert response.path() == expected_path

    # Additional test methods can be added here, following the same structure and pattern as above.