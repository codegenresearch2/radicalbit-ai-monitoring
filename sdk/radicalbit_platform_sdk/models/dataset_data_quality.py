from typing import List, Optional, Union\\\nfrom pydantic import BaseModel, ConfigDict\\\\\nclass Histogram(BaseModel):\"buckets": List[float]\"reference_values": List[int]\"current_values": Optional[List[int]] = None\\\\\n    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())\\\\\n\\\\nclass ClassMetrics(BaseModel):\"name": str\"count": int\"percentage": Optional[float] = None\\\\\n    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)\\\\\n\\\\nclass MedianMetrics(BaseModel):\"perc_25": Optional[float] = None\"median": Optional[float] = None\"perc_75": Optional[float] = None\\\\\n    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())\\\\\n\\\\nclass MissingValue(BaseModel):\"count": int\"percentage": Optional[float] = None\\\\\n    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())\\\\\n\\\\nclass ClassMedianMetrics(BaseModel):\"name": str\"mean": Optional[float] = None\"median_metrics": MedianMetrics\\\\\n    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())\\\\\n\\\\nclass FeatureMetrics(BaseModel):\"feature_name": str\"type": str\"missing_value": MissingValue\\\\\n    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())\\\\\n\\\\nclass NumericalFeatureMetrics(FeatureMetrics):\"type": str = 'numerical'\"mean": Optional[float] = None\"std": Optional[float] = None\"min": Optional[float] = None\"max": Optional[float] = None\"median_metrics": MedianMetrics\"class_median_metrics": List[ClassMedianMetrics]\"histogram": Histogram\\\\\n    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())\\\\\n\\\\nclass CategoryFrequency(BaseModel):\"name": str\"count": int\"frequency": Optional[float] = None\\\\\n    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())\\\\\n\\\\nclass CategoricalFeatureMetrics(FeatureMetrics):\"type": str = 'categorical'\"category_frequency": List[CategoryFrequency]\"distinct_value": int\\\\\n    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())\\\\\n\\\\nclass DataQuality(BaseModel):\"pass"\\\\n\\\\nclass BinaryClassificationDataQuality(DataQuality):\"n_observations": int\"class_metrics": List[ClassMetrics]\"feature_metrics": List[Union[NumericalFeatureMetrics, CategoricalFeatureMetrics]]\\\\\n    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, alias_generator=to_camel, protected_namespaces=())\\\\\n\\\\nclass MultiClassDataQuality(DataQuality):\"pass"\\\\n\\\\nclass RegressionDataQuality(DataQuality):\"pass"\\\\n