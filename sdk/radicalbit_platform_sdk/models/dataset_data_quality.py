from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import List, Union


class MedianMetrics(BaseModel):
    perc_25: Union[float, None] = None
    median: Union[float, None] = None
    perc_75: Union[float, None] = None

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )


class MissingValue(BaseModel):
    count: int
    percentage: Union[float, None] = None

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )


class ClassMedianMetrics(BaseModel):
    name: str
    mean: Union[float, None] = None
    median_metrics: MedianMetrics

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )


class FeatureMetrics(BaseModel):
    feature_name: str
    type: str
    missing_value: MissingValue

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )


class NumericalFeatureMetrics(FeatureMetrics):
    type: str = 'numerical'
    mean: float
    std: float
    min: float
    max: float
    median_metrics: MedianMetrics
    class_median_metrics: List[ClassMedianMetrics]

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )


class CategoryFrequency(BaseModel):
    name: str
    count: int
    frequency: Union[float, None] = None

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )


class CategoricalFeatureMetrics(FeatureMetrics):
    type: str = 'categorical'
    category_frequency: List[CategoryFrequency]
    distinct_value: int

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
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
        alias_generator=to_camel,
    )


class MultiClassDataQuality(DataQuality):
    pass


class RegressionDataQuality(DataQuality):
    pass
