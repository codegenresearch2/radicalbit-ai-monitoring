from radicalbit_platform_sdk.commons import invoke
from radicalbit_platform_sdk.models import (
    JobStatus,
    ReferenceFileUpload,
    DatasetStats,
    ModelQuality,
    DataQuality,
    ModelType,
    BinaryClassificationModelQuality,
    BinaryClassificationDataQuality,
)
from radicalbit_platform_sdk.errors import ClientError
from pydantic import ValidationError
from typing import Optional, Callable, Tuple
import requests
from uuid import UUID


class ModelReferenceDataset:
    def __init__(
        self,
        base_url: str,
        model_uuid: UUID,
        model_type: ModelType,
        upload: ReferenceFileUpload,
    ) -> None:
        self.__base_url = base_url
        self.__model_uuid = model_uuid
        self.__model_type = model_type
        self.__uuid = upload.uuid
        self.__path = upload.path
        self.__date = upload.date
        self.__status = upload.status
        self.__statistics = None
        self.__model_metrics = None
        self.__data_metrics = None

    def uuid(self) -> UUID:
        return self.__uuid

    def path(self) -> str:
        return self.__path

    def date(self) -> str:
        return self.__date

    def status(self) -> str:
        return self.__status

    def statistics(self) -> Optional[DatasetStats]:
        """
        Get statistics about the current dataset

        :return: The `DatasetStats` if exists
        """
        if self.__status != JobStatus.SUCCEEDED:
            return None
        if self.__statistics is None:
            self.__statistics = self._fetch_statistics()
        return self.__statistics

    def data_quality(self) -> Optional[DataQuality]:
        """
        Get data quality metrics about the current dataset

        :return: The `DataQuality` if exists
        """
        if self.__status != JobStatus.SUCCEEDED:
            return None
        if self.__data_metrics is None:
            self.__data_metrics = self._fetch_data_quality()
        return self.__data_metrics

    def model_quality(self) -> Optional[ModelQuality]:
        """
        Get model quality metrics about the current dataset

        :return: The `ModelQuality` if exists
        """
        if self.__status != JobStatus.SUCCEEDED:
            return None
        if self.__model_metrics is None:
            self.__model_metrics = self._fetch_model_quality()
        return self.__model_metrics

    def _fetch_statistics(self) -> DatasetStats:
        response, _ = invoke(
            method="GET",
            url=f"{self.__base_url}/api/models/{str(self.__model_uuid)}/reference/statistics",
            valid_response_code=200,
        )
        return self._parse_statistics_response(response)

    def _fetch_data_quality(self) -> DataQuality:
        response, _ = invoke(
            method="GET",
            url=f"{self.__base_url}/api/models/{str(self.__model_uuid)}/reference/data-quality",
            valid_response_code=200,
        )
        return self._parse_data_quality_response(response)

    def _fetch_model_quality(self) -> ModelQuality:
        response, _ = invoke(
            method="GET",
            url=f"{self.__base_url}/api/models/{str(self.__model_uuid)}/reference/model-quality",
            valid_response_code=200,
        )
        return self._parse_model_quality_response(response)

    def _parse_statistics_response(self, response: requests.Response) -> DatasetStats:
        try:
            response_json = response.json()
            job_status = JobStatus(response_json["jobStatus"])
            if job_status != JobStatus.SUCCEEDED:
                raise ClientError(f"Job status is {job_status}")
            if "statistics" not in response_json:
                raise ClientError("Statistics not found in response")
            return DatasetStats.model_validate(response_json["statistics"])
        except KeyError as e:
            raise ClientError(f"Unable to parse response: {response.text}")
        except ValidationError as e:
            raise ClientError(f"Unable to parse response: {response.text}")

    def _parse_data_quality_response(self, response: requests.Response) -> DataQuality:
        try:
            response_json = response.json()
            job_status = JobStatus(response_json["jobStatus"])
            if job_status != JobStatus.SUCCEEDED:
                raise ClientError(f"Job status is {job_status}")
            if "dataQuality" not in response_json:
                raise ClientError("Data quality not found in response")
            if self.__model_type is ModelType.BINARY:
                return BinaryClassificationDataQuality.model_validate(
                    response_json["dataQuality"]
                )
            else:
                raise ClientError("Unable to parse get metrics for not binary models")
        except KeyError as e:
            raise ClientError(f"Unable to parse response: {response.text}")
        except ValidationError as e:
            raise ClientError(f"Unable to parse response: {response.text}")

    def _parse_model_quality_response(self, response: requests.Response) -> ModelQuality:
        try:
            response_json = response.json()
            job_status = JobStatus(response_json["jobStatus"])
            if job_status != JobStatus.SUCCEEDED:
                raise ClientError(f"Job status is {job_status}")
            if "modelQuality" not in response_json:
                raise ClientError("Model quality not found in response")
            if self.__model_type is ModelType.BINARY:
                return BinaryClassificationModelQuality.model_validate(
                    response_json["modelQuality"]
                )
            else:
                raise ClientError("Unable to parse get metrics for not binary models")
        except KeyError as e:
            raise ClientError(f"Unable to parse response: {response.text}")
        except ValidationError as e:
            raise ClientError(f"Unable to parse response: {response.text}")