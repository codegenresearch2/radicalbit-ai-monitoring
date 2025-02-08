from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import List, Optional, Union


class MedianMetrics(BaseModel):
    perc_25: Optional[float] = None
    median: Optional[float] = None
    perc_75: Optional[float] = None

    model_config = ConfigDict(
        populate_by_name=True,
    )


class MissingValue(BaseModel):
    count: int
    percentage: Optional[float] = None

    model_config = ConfigDict(
        populate_by_name=True,
    )


class ClassMedianMetrics(BaseModel):
    name: str
    mean: Optional[float] = None
    median_metrics: MedianMetrics

    model_config = ConfigDict(
        populate_by_name=True,
    )


class FeatureMetrics(BaseModel):
    feature_name: str
    type: str
    missing_value: MissingValue

    model_config = ConfigDict(
        populate_by_name=True,
    )


class NumericalFeatureMetrics(FeatureMetrics):
    type: str = 'numerical'
    mean: float
    std: float
    min: float
    max: float
    median_metrics: MedianMetrics
    class_median_metrics: List[ClassMedianMetrics]
    histogram: 'Histogram'  # Assuming the Histogram class is defined elsewhere

    model_config = ConfigDict(
        populate_by_name=True,
    )


class CategoryFrequency(BaseModel):
    name: str
    count: int
    frequency: Optional[float] = None

    model_config = ConfigDict(
        populate_by_name=True,
    )


class CategoricalFeatureMetrics(FeatureMetrics):
    type: str = 'categorical'
    category_frequency: List[CategoryFrequency]
    distinct_value: int

    model_config = ConfigDict(
        populate_by_name=True,
    )


class ClassMetrics(BaseModel):
    name: str
    count: int
    percentage: Optional[float] = None

    model_config = ConfigDict(
        populate_by_name=True,
    )


class Histogram(BaseModel):
    buckets: List[float]
    reference_values: List[int]
    current_values: Optional[List[int]] = None

    model_config = ConfigDict(
        populate_by_name=True,
    )


class DataQuality(BaseModel):
    pass


class BinaryClassificationDataQuality(DataQuality):
    n_observations: int
    class_metrics: List[ClassMetrics]
    feature_metrics: List[Union[NumericalFeatureMetrics, CategoricalFeatureMetrics]]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )


class MultiClassDataQuality(DataQuality):
    pass


class RegressionDataQuality(DataQuality):
    pass