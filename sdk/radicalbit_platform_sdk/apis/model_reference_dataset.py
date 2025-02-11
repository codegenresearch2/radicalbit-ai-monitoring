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
from typing import Optional, Callable
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
        if self.__status == JobStatus.ERROR:
            raise ClientError("The job has failed.")
        elif self.__status == JobStatus.SUCCEEDED:
            if self.__statistics is not None:
                return self.__statistics
            else:
                self.__statistics = self.__fetch_statistics()
                return self.__statistics
        elif self.__status == JobStatus.IMPORTING:
            self.__statistics = self.__fetch_statistics()
            return self.__statistics

    def __fetch_statistics(self) -> Optional[DatasetStats]:
        def __callback(response: requests.Response) -> Optional[DatasetStats]:
            try:
                response_json = response.json()
                job_status = JobStatus(response_json["jobStatus"])
                if "statistics" in response_json:
                    return DatasetStats.model_validate(response_json["statistics"])
                else:
                    return None
            except KeyError:
                raise ClientError("Unable to parse response: missing expected keys")
            except ValidationError:
                raise ClientError("Unable to parse response: invalid data structure")

        response = invoke(
            method="GET",
            url=f"{self.__base_url}/api/models/{str(self.__model_uuid)}/reference/statistics",
            valid_response_code=200,
            func=__callback,
        )
        return response

    def data_quality(self) -> Optional[DataQuality]:
        """
        Get data quality metrics about the current dataset

        :return: The `DataQuality` if exists
        """
        if self.__status == JobStatus.ERROR:
            raise ClientError("The job has failed.")
        elif self.__status == JobStatus.SUCCEEDED:
            if self.__data_metrics is not None:
                return self.__data_metrics
            else:
                self.__data_metrics = self.__fetch_data_quality()
                return self.__data_metrics
        elif self.__status == JobStatus.IMPORTING:
            self.__data_metrics = self.__fetch_data_quality()
            return self.__data_metrics

    def __fetch_data_quality(self) -> Optional[DataQuality]:
        def __callback(response: requests.Response) -> Optional[DataQuality]:
            try:
                response_json = response.json()
                job_status = JobStatus(response_json["jobStatus"])
                if "dataQuality" in response_json:
                    if self.__model_type is ModelType.BINARY:
                        return BinaryClassificationDataQuality.model_validate(response_json["dataQuality"])
                    else:
                        raise ClientError("Unable to parse get metrics for not binary models")
                else:
                    return None
            except KeyError:
                raise ClientError("Unable to parse response: missing expected keys")
            except ValidationError:
                raise ClientError("Unable to parse response: invalid data structure")

        response = invoke(
            method="GET",
            url=f"{self.__base_url}/api/models/{str(self.__model_uuid)}/reference/data-quality",
            valid_response_code=200,
            func=__callback,
        )
        return response

    def model_quality(self) -> Optional[ModelQuality]:
        """
        Get model quality metrics about the current dataset

        :return: The `ModelQuality` if exists
        """
        if self.__status == JobStatus.ERROR:
            raise ClientError("The job has failed.")
        elif self.__status == JobStatus.SUCCEEDED:
            if self.__model_metrics is not None:
                return self.__model_metrics
            else:
                self.__model_metrics = self.__fetch_model_quality()
                return self.__model_metrics
        elif self.__status == JobStatus.IMPORTING:
            self.__model_metrics = self.__fetch_model_quality()
            return self.__model_metrics

    def __fetch_model_quality(self) -> Optional[ModelQuality]:
        def __callback(response: requests.Response) -> Optional[ModelQuality]:
            try:
                response_json = response.json()
                job_status = JobStatus(response_json["jobStatus"])
                if "modelQuality" in response_json:
                    if self.__model_type is ModelType.BINARY:
                        return BinaryClassificationModelQuality.model_validate(response_json["modelQuality"])
                    else:
                        raise ClientError("Unable to parse get metrics for not binary models")
                else:
                    return None
            except KeyError:
                raise ClientError("Unable to parse response: missing expected keys")
            except ValidationError:
                raise ClientError("Unable to parse response: invalid data structure")

        response = invoke(
            method="GET",
            url=f"{self.__base_url}/api/models/{str(self.__model_uuid)}/reference/model-quality",
            valid_response_code=200,
            func=__callback,
        )
        return response