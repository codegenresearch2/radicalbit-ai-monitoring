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

class Model:
    def __init__(self, base_url: str, definition: ModelDefinition) -> None:
        self.base_url = base_url
        self.definition = definition

    def get_uuid(self) -> UUID:
        return self.definition.uuid

    def get_name(self) -> str:
        return self.definition.name

    def get_description(self) -> Optional[str]:
        return self.definition.description

    def get_model_type(self) -> ModelType:
        return self.definition.model_type

    def get_data_type(self) -> DataType:
        return self.definition.data_type

    def get_granularity(self) -> Granularity:
        return self.definition.granularity

    def get_features(self) -> List[ColumnDefinition]:
        return self.definition.features

    def get_target(self) -> ColumnDefinition:
        return self.definition.target

    def get_timestamp(self) -> ColumnDefinition:
        return self.definition.timestamp

    def get_outputs(self) -> OutputType:
        return self.definition.outputs

    def get_frameworks(self) -> Optional[str]:
        return self.definition.frameworks

    def get_algorithm(self) -> Optional[str]:
        return self.definition.algorithm

    def delete(self) -> None:
        invoke(
            method='DELETE',
            url=f'{self.base_url}/api/models/{str(self.get_uuid())}',
            valid_response_code=200,
            func=lambda _: None,
        )

    def get_reference_datasets(self) -> List[ModelReferenceDataset]:
        def callback(response: requests.Response) -> List[ModelReferenceDataset]:
            try:
                adapter = TypeAdapter(List[ReferenceFileUpload])
                references = adapter.validate_python(response.json())

                return [
                    ModelReferenceDataset(
                        self.base_url, self.get_uuid(), self.get_model_type(), ref
                    )
                    for ref in references
                ]
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e

        return invoke(
            method='GET',
            url=f'{self.base_url}/api/models/{str(self.get_uuid())}/reference/all',
            valid_response_code=200,
            func=callback,
        )

    def get_current_datasets(self) -> List[ModelCurrentDataset]:
        def callback(response: requests.Response) -> List[ModelCurrentDataset]:
            try:
                adapter = TypeAdapter(List[CurrentFileUpload])
                references = adapter.validate_python(response.json())

                return [
                    ModelCurrentDataset(
                        self.base_url, self.get_uuid(), self.get_model_type(), ref
                    )
                    for ref in references
                ]
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e

        return invoke(
            method='GET',
            url=f'{self.base_url}/api/models/{str(self.get_uuid())}/current/all',
            valid_response_code=200,
            func=callback,
        )

    def load_reference_dataset(
        self,
        file_name: str,
        bucket: str,
        object_name: Optional[str] = None,
        aws_credentials: Optional[AwsCredentials] = None,
        separator: str = ',',
    ) -> ModelReferenceDataset:
        file_headers = pd.read_csv(
            file_name, nrows=0, delimiter=separator
        ).columns.tolist()

        required_headers = self._get_required_headers()

        if set(required_headers).issubset(file_headers):
            if object_name is None:
                object_name = f'{self.get_uuid()}/reference/{os.path.basename(file_name)}'

            try:
                s3_client = self._get_s3_client(aws_credentials)

                s3_client.upload_file(
                    file_name,
                    bucket,
                    object_name,
                    ExtraArgs={
                        'Metadata': {
                            'model_uuid': str(self.get_uuid()),
                            'model_name': self.get_name(),
                            'file_type': 'reference',
                        }
                    },
                )
            except BotoClientError as e:
                raise ClientError(
                    f'Unable to upload file {file_name} to remote storage: {e}'
                ) from e
            return self._bind_reference_dataset(
                f's3://{bucket}/{object_name}', separator
            )

        raise ClientError(
            f'File {file_name} does not contain all defined columns: {required_headers}'
        ) from None

    def bind_reference_dataset(
        self,
        dataset_url: str,
        aws_credentials: Optional[AwsCredentials] = None,
        separator: str = ',',
    ) -> ModelReferenceDataset:
        url_parts = dataset_url.replace('s3://', '').split('/')

        try:
            s3_client = self._get_s3_client(aws_credentials)

            chunks_iterator = s3_client.get_object(
                Bucket=url_parts[0], Key='/'.join(url_parts[1:])
            )['Body'].iter_chunks()

            chunks = ''
            for c in (chunk for chunk in chunks_iterator if '\n' not in chunks):
                chunks += c.decode('UTF-8')

            file_headers = chunks.split('\n')[0].split(separator)

            required_headers = self._get_required_headers()

            if set(required_headers).issubset(file_headers):
                return self._bind_reference_dataset(dataset_url, separator)

            raise ClientError(
                f'File {dataset_url} does not contain all defined columns: {required_headers}'
            ) from None
        except BotoClientError as e:
            raise ClientError(
                f'Unable to get file {dataset_url} from remote storage: {e}'
            ) from e

    def load_current_dataset(
        self,
        file_name: str,
        bucket: str,
        correlation_id_column: Optional[str] = None,
        object_name: Optional[str] = None,
        aws_credentials: Optional[AwsCredentials] = None,
        separator: str = ',',
    ) -> ModelCurrentDataset:
        file_headers = pd.read_csv(
            file_name, nrows=0, delimiter=separator
        ).columns.tolist()

        required_headers = self._get_required_headers()
        if correlation_id_column:
            required_headers.append(correlation_id_column)
        required_headers.append(self.get_timestamp().name)

        if set(required_headers).issubset(file_headers):
            if object_name is None:
                object_name = f'{self.get_uuid()}/current/{os.path.basename(file_name)}'

            try:
                s3_client = self._get_s3_client(aws_credentials)

                s3_client.upload_file(
                    file_name,
                    bucket,
                    object_name,
                    ExtraArgs={
                        'Metadata': {
                            'model_uuid': str(self.get_uuid()),
                            'model_name': self.get_name(),
                            'file_type': 'current',
                        }
                    },
                )
            except BotoClientError as e:
                raise ClientError(
                    f'Unable to upload file {file_name} to remote storage: {e}'
                ) from e
            return self._bind_current_dataset(
                f's3://{bucket}/{object_name}', separator, correlation_id_column
            )

        raise ClientError(
            f'File {file_name} does not contain all defined columns: {required_headers}'
        ) from None

    def bind_current_dataset(
        self,
        dataset_url: str,
        correlation_id_column: str,
        aws_credentials: Optional[AwsCredentials] = None,
        separator: str = ',',
    ) -> ModelCurrentDataset:
        url_parts = dataset_url.replace('s3://', '').split('/')

        try:
            s3_client = self._get_s3_client(aws_credentials)

            chunks_iterator = s3_client.get_object(
                Bucket=url_parts[0], Key='/'.join(url_parts[1:])
            )['Body'].iter_chunks()

            chunks = ''
            for c in (chunk for chunk in chunks_iterator if '\n' not in chunks):
                chunks += c.decode('UTF-8')

            file_headers = chunks.split('\n')[0].split(separator)

            required_headers = self._get_required_headers()
            required_headers.append(correlation_id_column)
            required_headers.append(self.get_timestamp().name)

            if set(required_headers).issubset(file_headers):
                return self._bind_current_dataset(
                    dataset_url, separator, correlation_id_column
                )

            raise ClientError(
                f'File {dataset_url} does not contain all defined columns: {required_headers}'
            ) from None
        except BotoClientError as e:
            raise ClientError(
                f'Unable to get file {dataset_url} from remote storage: {e}'
            ) from e

    def _bind_reference_dataset(
        self,
        dataset_url: str,
        separator: str,
    ) -> ModelReferenceDataset:
        def callback(response: requests.Response) -> ModelReferenceDataset:
            try:
                response = ReferenceFileUpload.model_validate(response.json())
                return ModelReferenceDataset(
                    self.base_url, self.get_uuid(), self.get_model_type(), response
                )
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e

        file_ref = FileReference(file_url=dataset_url, separator=separator)

        return invoke(
            method='POST',
            url=f'{self.base_url}/api/models/{str(self.get_uuid())}/reference/bind',
            valid_response_code=200,
            func=callback,
            data=file_ref.model_dump_json(),
        )

    def _bind_current_dataset(
        self,
        dataset_url: str,
        separator: str,
        correlation_id_column: Optional[str] = None,
    ) -> ModelCurrentDataset:
        def callback(response: requests.Response) -> ModelCurrentDataset:
            try:
                response = CurrentFileUpload.model_validate(response.json())
                return ModelCurrentDataset(
                    self.base_url, self.get_uuid(), self.get_model_type(), response
                )
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e

        file_ref = FileReference(
            file_url=dataset_url,
            separator=separator,
            correlation_id_column=correlation_id_column,
        )

        return invoke(
            method='POST',
            url=f'{self.base_url}/api/models/{str(self.get_uuid())}/current/bind',
            valid_response_code=200,
            func=callback,
            data=file_ref.model_dump_json(),
        )

    def _get_required_headers(self) -> List[str]:
        model_columns = self.get_features() + self.get_outputs().output
        model_columns.append(self.get_target())
        return [model_column.name for model_column in model_columns]

    def _get_s3_client(self, aws_credentials: Optional[AwsCredentials] = None):
        return boto3.client(
            's3',
            aws_access_key_id=(
                None if aws_credentials is None else aws_credentials.access_key_id
            ),
            aws_secret_access_key=(
                None
                if aws_credentials is None
                else aws_credentials.secret_access_key
            ),
            region_name=(
                None if aws_credentials is None else aws_credentials.default_region
            ),
            endpoint_url=(
                None
                if aws_credentials is None
                else (
                    None
                    if aws_credentials.endpoint_url is None
                    else aws_credentials.endpoint_url
                )
            ),
        )