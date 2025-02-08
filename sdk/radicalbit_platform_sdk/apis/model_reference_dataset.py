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
    def __init__(self,
                 base_url: str,
                 model_uuid: UUID,
                 model_type: ModelType,
                 upload: ReferenceFileUpload,
                 ) -> None:
        self._base_url = base_url
        self._model_uuid = model_uuid
        self._model_type = model_type
        self._uuid = upload.uuid
        self._path = upload.path
        self._date = upload.date
        self._status = upload.status
        self._statistics = None
        self._model_metrics = None
        self._data_metrics = None

    def uuid(self) -> UUID:
        return self._uuid

    def path(self) -> str:
        return self._path

    def date(self) -> str:
        return self._date

    def status(self) -> str:
        return self._status

    def statistics(self) -> Optional[DatasetStats]:
        """
        Get statistics about the current dataset

        :return: The `DatasetStats` if exists
        """

        def __callback(response: requests.Response) -> tuple[JobStatus, Optional[DatasetStats]]:
            try:
                response_json = response.json()
                job_status = JobStatus(response_json["jobStatus"])
                if "statistics" in response_json:
                    return job_status, DatasetStats.model_validate(response_json["statistics"])
                else:
                    return job_status, None
            except KeyError as _:
                raise ClientError(f"Unable to parse response: {response.text}")
            except ValidationError as _:
                raise ClientError(f"Unable to parse response: {response.text}")

        if self._status == JobStatus.ERROR:
            self._statistics = None
        elif self._status == JobStatus.SUCCEEDED:
            if self._statistics is None:
                _, stats = invoke(
                    method="GET",
                    url=f"{self._base_url}/api/models/{str(self._model_uuid)}/reference/statistics",
                    valid_response_code=200,
                    func=__callback,
                )
                self._statistics = stats
        elif self._status == JobStatus.IMPORTING:
            status, stats = invoke(
                method="GET",
                url=f"{self._base_url}/api/models/{str(self._model_uuid)}/reference/statistics",
                valid_response_code=200,
                func=__callback,
            )
            self._status = status
            self._statistics = stats

        return self._statistics

    def data_quality(self) -> Optional[DataQuality]:
        """
        Get data quality metrics about the current dataset

        :return: The `DataQuality` if exists
        """

        def __callback(response: requests.Response) -> Optional[DataQuality]:
            try:
                response_json = response.json()
                job_status = JobStatus(response_json["jobStatus"])
                if "dataQuality" in response_json:
                    if self._model_type is ModelType.BINARY:
                        return job_status, BinaryClassificationDataQuality.model_validate(response_json["dataQuality"])
                    else:
                        raise ClientError("Unable to parse get metrics for not binary models")
                else:
                    return job_status, None
            except KeyError as _:
                raise ClientError(f"Unable to parse response: {response.text}")
            except ValidationError as _:
                raise ClientError(f"Unable to parse response: {response.text}")

        if self._status == JobStatus.ERROR:
            self._data_metrics = None
        elif self._status == JobStatus.SUCCEEDED:
            if self._data_metrics is None:
                _, metrics = invoke(
                    method="GET",
                    url=f"{self._base_url}/api/models/{str(self._model_uuid)}/reference/data-quality",
                    valid_response_code=200,
                    func=__callback,
                )
                self._data_metrics = metrics
        elif self._status == JobStatus.IMPORTING:
            status, metrics = invoke(
                method="GET",
                url=f"{self._base_url}/api/models/{str(self._model_uuid)}/reference/data-quality",
                valid_response_code=200,
                func=__callback,
            )
            self._status = status
            self._data_metrics = metrics

        return self._data_metrics

    def model_quality(self) -> Optional[ModelQuality]:
        """
        Get model quality metrics about the current dataset

        :return: The `ModelQuality` if exists
        """

        def __callback(response: requests.Response) -> tuple[JobStatus, Optional[ModelQuality]]:
            try:
                response_json = response.json()
                job_status = JobStatus(response_json["jobStatus"])
                if "modelQuality" in response_json:
                    if self._model_type is ModelType.BINARY:
                        return job_status, BinaryClassificationModelQuality.model_validate(response_json["modelQuality"])
                    else:
                        raise ClientError("Unable to parse get metrics for not binary models")
                else:
                    return job_status, None
            except KeyError as _:
                raise ClientError(f"Unable to parse response: {response.text}")
            except ValidationError as _:
                raise ClientError(f"Unable to parse response: {response.text}")

        if self._status == JobStatus.ERROR:
            self._model_metrics = None
        elif self._status == JobStatus.SUCCEEDED:
            if self._model_metrics is None:
                _, metrics = invoke(
                    method="GET",
                    url=f"{self._base_url}/api/models/{str(self._model_uuid)}/reference/model-quality",
                    valid_response_code=200,
                    func=__callback,
                )
                self._model_metrics = metrics
        elif self._status == JobStatus.IMPORTING:
            status, metrics = invoke(
                method="GET",
                url=f"{self._base_url}/api/models/{str(self._model_uuid)}/reference/model-quality",
                valid_response_code=200,
                func=__callback,
            )
            self._status = status
            self._model_metrics = metrics

        return self._model_metrics
