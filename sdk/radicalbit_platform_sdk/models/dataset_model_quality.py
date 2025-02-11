from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Optional

class ModelQuality(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())

class BinaryClassificationModelQuality(ModelQuality):
    f1: Optional[float] = None
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f_measure: Optional[float] = None
    weighted_precision: Optional[float] = None
    weighted_recall: Optional[float] = None
    weighted_f_measure: Optional[float] = None
    weighted_true_positive_rate: Optional[float] = None
    weighted_false_positive_rate: Optional[float] = None
    true_positive_rate: Optional[float] = None
    false_positive_rate: Optional[float] = None
    true_positive_count: Optional[int] = None
    false_positive_count: Optional[int] = None
    true_negative_count: Optional[int] = None
    false_negative_count: Optional[int] = None
    area_under_roc: Optional[float] = None
    area_under_pr: Optional[float] = None

class MultiClassModelQuality(ModelQuality):
    pass

class RegressionModelQuality(ModelQuality):
    pass