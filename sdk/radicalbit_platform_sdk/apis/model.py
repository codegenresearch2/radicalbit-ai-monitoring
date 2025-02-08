import os\"\nfrom typing import List, Optional, TypeAlias\nimport uuid\nimport boto3\nfrom botocore.exceptions import ClientError\nimport pandas as pd\nfrom pydantic import TypeAdapter, ValidationError\nimport requests\n\n\nclass Model:\n    def __init__(self, base_url: str, definition: ModelDefinition) -> None:\n        self.__base_url = base_url\n        self.__uuid = definition.uuid\n        self.__name = definition.name\n        self.__description = definition.description\n        self.__model_type = definition.model_type\n        self.__data_type = definition.data_type\n        self.__granularity = definition.granularity\n        self.__features = definition.features\n        self.__target = definition.target\n        self.__timestamp = definition.timestamp\n        self.__outputs = definition.outputs\n        self.__frameworks = definition.frameworks\n        self.__algorithm = definition.algorithm\n\n    def uuid(self) -> UUID:\n        return self.__uuid\n\n    def name(self) -> str:\n        return self.__name\n\n    def description(self) -> Optional[str]:\n        return self.__description\n\n    def model_type(self) -> ModelType:\n        return self.__model_type\n\n    def data_type(self) -> DataType:\n        return self.__data_type\n\n    def granularity(self) -> Granularity:\n        return self.__granularity\n\n    def features(self) -> List[ColumnDefinition]:\n        return self.__features\n\n    def target(self) -> ColumnDefinition:\n        return self.__target\n\n    def timestamp(self) -> ColumnDefinition:\n        return self.__timestamp\n\n    def outputs(self) -> OutputType:\n        return self.__outputs\n\n    def frameworks(self) -> Optional[str]:\n        return self.__frameworks\n\n    def algorithm(self) -> Optional[str]:\n        return self.__algorithm\n\n    def delete(self) -> None:\n        invoke(\n            method='DELETE',\n            url=f'{self.__base_url}/api/models/{str(self.__uuid)}',\n            valid_response_code=200,\n            func=lambda _: None,\n        )\n\n    def get_reference_datasets(self) -> List[ModelReferenceDataset]:\n        def __callback(response: requests.Response) -> List[ModelReferenceDataset]:\n            try:\n                adapter = TypeAdapter(List[ReferenceFileUpload])\n                references = adapter.validate_python(response.json())\n\n                return [\n                    ModelReferenceDataset(self.__base_url, self.__uuid, self.__model_type, ref)\n                    for ref in references\n                ]\n            except ValidationError as e:\n                raise ClientError(f'Unable to parse response: {response.text}') from e\n\n        return invoke(\n            method='GET',\n            url=f'{self.__base_url}/api/models/{str(self.__uuid)}/reference/all',\n            valid_response_code=200,\n            func=__callback,\n        )\n\n    # Additional methods for load_reference_dataset, load_current_dataset, etc. would be defined here.\n\n\n# Assuming ModelDefinition, ModelType, DataType, etc. are defined elsewhere in the code.\n\n# Example of a type alias for better readability\nColumnDefinitionList: TypeAlias = List[ColumnDefinition]\n