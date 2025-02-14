from pydantic import BaseModel, ConfigDict, validator
from pydantic.alias_generators import to_camel
from typing import List, Optional, Union

class ClassMetrics(BaseModel):
    name: str
    count: int
    percentage: Optional[float] = None

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    @validator('percentage', pre=True, always=True)
    def check_percentage(cls, v):
        if v is not None and not (0 <= v <= 100):
            raise ValueError('Percentage must be between 0 and 100')
        return v

class MedianMetrics(BaseModel):
    perc_25: Optional[float] = None
    median: Optional[float] = None
    perc_75: Optional[float] = None

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())

class MissingValue(BaseModel):
    count: int
    percentage: Optional[float] = None

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())

    @validator('percentage', pre=True, always=True)
    def check_percentage(cls, v):
        if v is not None and not (0 <= v <= 100):
            raise ValueError('Percentage must be between 0 and 100')
        return v

class ClassMedianMetrics(BaseModel):
    name: str
    mean: Optional[float] = None
    median_metrics: MedianMetrics

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())

class FeatureMetrics(BaseModel):
    feature_name: str
    type: str
    missing_value: MissingValue

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())

class NumericalFeatureMetrics(FeatureMetrics):
    type: str = "numerical"
    mean: Optional[float] = None
    std: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None
    median_metrics: MedianMetrics
    class_median_metrics: List[ClassMedianMetrics]

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())

class CategoryFrequency(BaseModel):
    name: str
    count: int
    frequency: Optional[float] = None

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())

    @validator('frequency', pre=True, always=True)
    def check_frequency(cls, v):
        if v is not None and not (0 <= v <= 1):
            raise ValueError('Frequency must be between 0 and 1')
        return v

class CategoricalFeatureMetrics(FeatureMetrics):
    type: str = "categorical"
    category_frequency: List[CategoryFrequency]
    distinct_value: int

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())

class DataQuality(BaseModel):
    pass

class BinaryClassificationDataQuality(DataQuality):
    n_observations: int
    class_metrics: List[ClassMetrics]
    feature_metrics: List[Union[NumericalFeatureMetrics, CategoricalFeatureMetrics]]

    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, alias_generator=to_camel, protected_namespaces=())

class MultiClassDataQuality(DataQuality):
    pass

class RegressionDataQuality(DataQuality):
    pass

I've rewritten the code according to the provided rules. I've made the following changes:

1. Made optional all the fields that the user prefers for flexibility in data models.
2. Added validators to ensure that percentage values are between 0 and 100, and frequency values are between 0 and 1.
3. Made the `feature_metrics` field in `BinaryClassificationDataQuality` a Union type, allowing it to be either a `NumericalFeatureMetrics` or a `CategoricalFeatureMetrics` object.

These changes should improve error handling for API responses and allow for more flexibility in the data models. However, it's important to note that this code does not include comprehensive testing for new functionality. This would require additional code and is outside the scope of the current request.