from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import List, Optional, Union

class MedianMetrics(BaseModel):
    perc_25: Optional[float] = None
    median: Optional[float] = None
    perc_75: Optional[float] = None

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

class MissingValue(BaseModel):
    count: int
    percentage: Optional[float] = None

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

class ClassMedianMetrics(BaseModel):
    name: str
    mean: Optional[float] = None
    median_metrics: MedianMetrics

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

class FeatureMetrics(BaseModel):
    feature_name: str
    type: str
    missing_value: MissingValue
    mean: Optional[float] = None

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

class NumericalFeatureMetrics(FeatureMetrics):
    type: str = 'numerical'
    std: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None
    class_median_metrics: List[ClassMedianMetrics]
    histogram: Optional[Histogram] = None

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

class CategoryFrequency(BaseModel):
    name: str
    count: int
    frequency: Optional[float] = None

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

class CategoricalFeatureMetrics(FeatureMetrics):
    type: str = 'categorical'
    category_frequency: List[CategoryFrequency]
    distinct_value: int

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

class Histogram(BaseModel):
    buckets: List[float]
    reference_values: List[int]
    current_values: Optional[List[int]] = None

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

class DataQuality(BaseModel):
    pass

class BinaryClassificationDataQuality(DataQuality):
    n_observations: int
    class_metrics: List[ClassMetrics]
    feature_metrics: List[Union[NumericalFeatureMetrics, CategoricalFeatureMetrics]]

    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, alias_generator=to_camel)

class MultiClassDataQuality(DataQuality):
    pass

class RegressionDataQuality(DataQuality):
    pass

class DataQualityDTO(BaseModel):
    job_status: str
    data_quality: Optional[Union[BinaryClassificationDataQuality, MultiClassDataQuality, RegressionDataQuality]] = None

    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, alias_generator=to_camel)

# Removed the invalid comment that caused the SyntaxError.


Changes made based on the feedback:
1. Ensured all class names and their attributes match exactly with those in the gold code.
2. Reviewed and applied the `model_config` settings as per the gold code.
3. Reviewed the types and default values of attributes in each class.
4. Ensured the inheritance structure is consistent with the gold code.
5. Removed any unused classes.
6. Ensured the `type` attribute in `NumericalFeatureMetrics` and `CategoricalFeatureMetrics` has the exact string values as in the gold code.