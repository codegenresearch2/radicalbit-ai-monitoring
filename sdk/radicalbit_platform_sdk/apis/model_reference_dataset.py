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
from typing import Optional
import requests
from uuid import UUID


class ModelReferenceDataset:
    def __init__(
        self,
        base_url: str,
        model_uuid: UUID,
        model_type: ModelType,
        upload: ReferenceFileUpload,
        statistics: Optional[DatasetStats] = None,
        model_metrics: Optional[ModelQuality] = None,
        data_metrics: Optional[DataQuality] = None,
    ) -> None:
        self.__base_url = base_url
        self.__model_uuid = model_uuid
        self.__model_type = model_type
        self.__uuid = upload.uuid
        self.__path = upload.path
        self.__date = upload.date
        self.__status = upload.status
        self.__statistics = statistics
        self.__model_metrics = model_metrics
        self.__data_metrics = data_metrics

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
        if self.__statistics is None and self.__status == JobStatus.SUCCEEDED:
            self.__statistics = self._fetch_statistics()
        return self.__statistics

    def data_quality(self) -> Optional[DataQuality]:
        """
        Get data quality metrics about the current dataset

        :return: The `DataQuality` if exists
        """
        if self.__data_metrics is None and self.__status == JobStatus.SUCCEEDED:
            self.__data_metrics = self._fetch_data_quality()
        return self.__data_metrics

    def model_quality(self) -> Optional[ModelQuality]:
        """
        Get model quality metrics about the current dataset

        :return: The `ModelQuality` if exists
        """
        if self.__model_metrics is None and self.__status == JobStatus.SUCCEEDED:
            self.__model_metrics = self._fetch_model_quality()
        return self.__model_metrics

    def _fetch_statistics(self) -> DatasetStats:
        _, stats = invoke(
            method="GET",
            url=f"{self.__base_url}/api/models/{str(self.__model_uuid)}/reference/statistics",
            valid_response_code=200,
            func=self._parse_statistics_response,
        )
        return stats

    def _fetch_data_quality(self) -> DataQuality:
        _, metrics = invoke(
            method="GET",
            url=f"{self.__base_url}/api/models/{str(self.__model_uuid)}/reference/data-quality",
            valid_response_code=200,
            func=self._parse_data_quality_response,
        )
        return metrics

    def _fetch_model_quality(self) -> ModelQuality:
        _, metrics = invoke(
            method="GET",
            url=f"{self.__base_url}/api/models/{str(self.__model_uuid)}/reference/model-quality",
            valid_response_code=200,
            func=self._parse_model_quality_response,
        )
        return metrics

    def _parse_statistics_response(self, response: requests.Response) -> DatasetStats:
        try:
            response_json = response.json()
            job_status = JobStatus(response_json["jobStatus"])
            if "statistics" in response_json:
                return DatasetStats.model_validate(response_json["statistics"])
            else:
                return None
        except KeyError as e:
            raise ClientError(f"Unable to parse response: {response.text}")
        except ValidationError as e:
            raise ClientError(f"Unable to parse response: {response.text}")

    def _parse_data_quality_response(self, response: requests.Response) -> DataQuality:
        try:
            response_json = response.json()
            job_status = JobStatus(response_json["jobStatus"])
            if "dataQuality" in response_json:
                if self.__model_type is ModelType.BINARY:
                    return BinaryClassificationDataQuality.model_validate(
                        response_json["dataQuality"]
                    )
                else:
                    raise ClientError(
                        "Unable to parse get metrics for not binary models"
                    )
            else:
                return None
        except KeyError as e:
            raise ClientError(f"Unable to parse response: {response.text}")
        except ValidationError as e:
            raise ClientError(f"Unable to parse response: {response.text}")

    def _parse_model_quality_response(self, response: requests.Response) -> ModelQuality:
        try:
            response_json = response.json()
            job_status = JobStatus(response_json["jobStatus"])
            if "modelQuality" in response_json:
                if self.__model_type is ModelType.BINARY:
                    return BinaryClassificationModelQuality.model_validate(
                        response_json["modelQuality"]
                    )
                else:
                    raise ClientError(
                        "Unable to parse get metrics for not binary models"
                    )
            else:
                return None
        except KeyError as e:
            raise ClientError(f"Unable to parse response: {response.text}")
        except ValidationError as e:
            raise ClientError(f"Unable to parse response: {response.text}")