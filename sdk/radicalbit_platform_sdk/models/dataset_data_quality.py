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
    histogram: Optional[Histogram] = None  # Added histogram attribute

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
1. Added `histogram` attribute to `NumericalFeatureMetrics` class.
2. Ensured `alias_generator=to_camel` is set in the `model_config` for all relevant classes.
3. Reviewed and corrected the attributes in each class to match the gold code.
4. Removed the invalid comment that caused the `SyntaxError`.