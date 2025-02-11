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
    ) -> None:
        self.base_url = base_url
        self.model_uuid = model_uuid
        self.model_type = model_type
        self.uuid = upload.uuid
        self.path = upload.path
        self.date = upload.date
        self.status = upload.status
        self.statistics = None
        self.model_metrics = None
        self.data_metrics = None

    def get_uuid(self) -> UUID:
        return self.uuid

    def get_path(self) -> str:
        return self.path

    def get_date(self) -> str:
        return self.date

    def get_status(self) -> str:
        return self.status

    def get_statistics(self) -> Optional[DatasetStats]:
        """
        Get statistics about the current dataset

        :return: The `DatasetStats` if exists
        """

        def __callback(
            response: requests.Response,
        ) -> tuple[JobStatus, Optional[DatasetStats]]:
            try:
                response_json = response.json()
                job_status = JobStatus(response_json["jobStatus"])
                if "statistics" in response_json:
                    return job_status, DatasetStats.model_validate(
                        response_json["statistics"]
                    )
                else:
                    return job_status, None
            except KeyError as _:
                raise ClientError(f"Unable to parse response: {response.text}")
            except ValidationError as _:
                raise ClientError(f"Unable to parse response: {response.text}")

        if self.status == JobStatus.ERROR:
            self.statistics = None
        elif self.status == JobStatus.SUCCEEDED and self.statistics is None:
            _, stats = invoke(
                method="GET",
                url=f"{self.base_url}/api/models/{str(self.model_uuid)}/reference/statistics",
                valid_response_code=200,
                func=__callback,
            )
            self.statistics = stats
        elif self.status == JobStatus.IMPORTING:
            status, stats = invoke(
                method="GET",
                url=f"{self.base_url}/api/models/{str(self.model_uuid)}/reference/statistics",
                valid_response_code=200,
                func=__callback,
            )
            self.status = status
            self.statistics = stats

        return self.statistics

    def get_data_quality(self) -> Optional[DataQuality]:
        """
        Get data quality metrics about the current dataset

        :return: The `DataQuality` if exists
        """

        def __callback(response: requests.Response) -> Optional[DataQuality]:
            try:
                response_json = response.json()
                job_status = JobStatus(response_json["jobStatus"])
                if "dataQuality" in response_json:
                    if self.model_type is ModelType.BINARY:
                        return (
                            job_status,
                            BinaryClassificationDataQuality.model_validate(
                                response_json["dataQuality"]
                            ),
                        )
                    else:
                        raise ClientError(
                            "Unable to parse get metrics for not binary models"
                        )
                else:
                    return job_status, None
            except KeyError as _:
                raise ClientError(f"Unable to parse response: {response.text}")
            except ValidationError as _:
                raise ClientError(f"Unable to parse response: {response.text}")

        if self.status == JobStatus.ERROR:
            self.data_metrics = None
        elif self.status == JobStatus.SUCCEEDED and self.data_metrics is None:
            _, metrics = invoke(
                method="GET",
                url=f"{self.base_url}/api/models/{str(self.model_uuid)}/reference/data-quality",
                valid_response_code=200,
                func=__callback,
            )
            self.data_metrics = metrics
        elif self.status == JobStatus.IMPORTING:
            status, metrics = invoke(
                method="GET",
                url=f"{self.base_url}/api/models/{str(self.model_uuid)}/reference/data-quality",
                valid_response_code=200,
                func=__callback,
            )
            self.status = status
            self.data_metrics = metrics

        return self.data_metrics

    def get_model_quality(self) -> Optional[ModelQuality]:
        """
        Get model quality metrics about the current dataset

        :return: The `ModelQuality` if exists
        """

        def __callback(
            response: requests.Response,
        ) -> tuple[JobStatus, Optional[ModelQuality]]:
            try:
                response_json = response.json()
                job_status = JobStatus(response_json["jobStatus"])
                if "modelQuality" in response_json:
                    if self.model_type is ModelType.BINARY:
                        return (
                            job_status,
                            BinaryClassificationModelQuality.model_validate(
                                response_json["modelQuality"]
                            ),
                        )
                    else:
                        raise ClientError(
                            "Unable to parse get metrics for not binary models"
                        )
                else:
                    return job_status, None
            except KeyError as _:
                raise ClientError(f"Unable to parse response: {response.text}")
            except ValidationError as _:
                raise ClientError(f"Unable to parse response: {response.text}")

        if self.status == JobStatus.ERROR:
            self.model_metrics = None
        elif self.status == JobStatus.SUCCEEDED and self.model_metrics is None:
            _, metrics = invoke(
                method="GET",
                url=f"{self.base_url}/api/models/{str(self.model_uuid)}/reference/model-quality",
                valid_response_code=200,
                func=__callback,
            )
            self.model_metrics = metrics
        elif self.status == JobStatus.IMPORTING:
            status, metrics = invoke(
                method="GET",
                url=f"{self.base_url}/api/models/{str(self.model_uuid)}/reference/model-quality",
                valid_response_code=200,
                func=__callback,
            )
            self.status = status
            self.model_metrics = metrics

        return self.model_metrics