from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import List, Optional, Union


class DatasetStats(BaseModel):
    n_variables: int
    n_observations: int
    missing_cells: int
    missing_cells_perc: Optional[float] = None
    duplicate_rows: int
    duplicate_rows_perc: Optional[float] = None
    numeric: int
    categorical: int
    datetime: int

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )