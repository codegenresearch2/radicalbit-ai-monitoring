from pydantic import BaseModel, ConfigDict\nfrom pydantic.alias_generators import to_camel\nfrom typing import List, Optional, Union\n\nclass MedianMetrics(BaseModel):\n    perc_25: Optional[float] = None\n    median: Optional[float] = None\n    perc_75: Optional[float] = None\n    \n    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())\n\nclass MissingValue(BaseModel):\n    count: int\n    percentage: Optional[float] = None\n    \n    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())\n\nclass ClassMedianMetrics(BaseModel):\n    name: str\n    mean: Optional[float] = None\n    median_metrics: MedianMetrics\n    \n    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())\n\nclass FeatureMetrics(BaseModel):\n    feature_name: str\n    type: str\n    missing_value: MissingValue\n    \n    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())\n\nclass NumericalFeatureMetrics(FeatureMetrics):\n    type: str = 'numerical'\n    mean: Optional[float] = None\n    std: Optional[float] = None\n    min: Optional[float] = None\n    max: Optional[float] = None\n    median_metrics: MedianMetrics\n    class_median_metrics: List[ClassMedianMetrics]\n    histogram: Optional[Histogram] = None\n    \n    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())\n\nclass CategoryFrequency(BaseModel):\n    name: str\n    count: int\n    frequency: Optional[float] = None\n    \n    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())\n\nclass CategoricalFeatureMetrics(FeatureMetrics):\n    type: str = 'categorical'\n    category_frequency: List[CategoryFrequency]\n    distinct_value: int\n    \n    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())\n\nclass Histogram(BaseModel):\n    buckets: List[float]\n    reference_values: List[int]\n    current_values: Optional[List[int]] = None\n    \n    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, protected_namespaces=())\n\nclass ClassMetrics(BaseModel):\n    name: str\n    count: int\n    percentage: Optional[float] = None\n    \n    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)\n\nclass BinaryClassificationDataQuality(BaseModel):\n    n_observations: int\n    class_metrics: List[ClassMetrics]\n    feature_metrics: List[Union[NumericalFeatureMetrics, CategoricalFeatureMetrics]]\n    \n    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, alias_generator=to_camel, protected_namespaces=())\n\nclass MultiClassDataQuality(BaseModel):\n    pass\n\nclass RegressionDataQuality(BaseModel):\n    pass\n