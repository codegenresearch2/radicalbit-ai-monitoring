from typing import List

from pyspark.ml.feature import StringIndexer
from pyspark.sql import DataFrame
from pyspark.sql.types import DoubleType, StructField, StructType

from models.reference_dataset import ReferenceDataset
from utils.models import ModelOut, ModelType, ColumnDefinition
from utils.spark import apply_schema_to_dataframe


class CurrentDataset:
    def __init__(self, model: ModelOut, raw_dataframe: DataFrame):
        current_schema = self.spark_schema(model)
        current_dataset = apply_schema_to_dataframe(raw_dataframe, current_schema)

        self.model = model
        self.current = current_dataset.select(
            *[c for c in current_schema.names if c in current_dataset.columns]
        )
        self.current_count = self.current.count()

    # FIXME this must exclude target when we will have separate current and ground truth
    @staticmethod
    def spark_schema(model: ModelOut):
        all_features = (
            model.features + [model.target] + [model.timestamp] + model.outputs.output
        )
        if model.outputs.prediction_proba and model.model_type == ModelType.BINARY:
            enforce_float = [
                model.target.name,
                model.outputs.prediction.name,
                model.outputs.prediction_proba.name,
            ]
        elif model.model_type == ModelType.BINARY:
            enforce_float = [model.target.name, model.outputs.prediction.name]
        else:
            enforce_float = []
        return StructType(
            [
                StructField(
                    name=feature.name,
                    dataType=model.convert_types(feature.type),
                    nullable=False,
                )
                if feature.name not in enforce_float
                else StructField(
                    name=feature.name,
                    dataType=DoubleType(),
                    nullable=False,
                )
                for feature in all_features
            ]
        )

    def get_numerical_features(self) -> List[ColumnDefinition]:
        return [feature for feature in self.model.features if feature.is_numerical()]

    def get_float_features(self) -> List[ColumnDefinition]:
        return [feature for feature in self.model.features if feature.is_float()]

    def get_int_features(self) -> List[ColumnDefinition]:
        return [feature for feature in self.model.features if feature.is_int()]

    def get_categorical_features(self) -> List[ColumnDefinition]:
        return [feature for feature in self.model.features if feature.is_categorical()]

    # FIXME this must exclude target when we will have separate current and ground truth
    def get_numerical_variables(self) -> List[ColumnDefinition]:
        all_features = (
            self.model.features
            + [self.model.target]
            + [self.model.timestamp]
            + self.model.outputs.output
        )
        return [feature for feature in all_features if feature.is_numerical()]

    # FIXME this must exclude target when we will have separate current and ground truth
    def get_categorical_variables(self) -> List[ColumnDefinition]:
        all_features = (
            self.model.features
            + [self.model.target]
            + [self.model.timestamp]
            + self.model.outputs.output
        )
        return [feature for feature in all_features if feature.is_categorical()]

    # FIXME this must exclude target when we will have separate current and ground truth
    def get_datetime_variables(self) -> List[ColumnDefinition]:
        all_features = (
            self.model.features
            + [self.model.target]
            + [self.model.timestamp]
            + self.model.outputs.output
        )
        return [feature for feature in all_features if feature.is_datetime()]

    # FIXME this must exclude target when we will have separate current and ground truth
    def get_all_variables(self) -> List[ColumnDefinition]:
        return (
            self.model.features
            + [self.model.target]
            + [self.model.timestamp]
            + self.model.outputs.output
        )

    def get_string_indexed_dataframe(self, reference: ReferenceDataset):
        """
        Source: https://stackoverflow.com/questions/65911146/how-to-transform-multiple-categorical-columns-to-integers-maintaining-shared-val
        Current dataset will be indexed with columns from both reference and current in order to have complete data
        """
        predictions_df_current = self.current.select(
            self.model.outputs.prediction.name
        ).withColumnRenamed(self.model.outputs.prediction.name, "classes")
        target_df_current = self.current.select(
            self.model.target.name
        ).withColumnRenamed(self.model.target.name, "classes")
        predictions_df_reference = reference.reference.select(
            self.model.outputs.prediction.name
        ).withColumnRenamed(self.model.outputs.prediction.name, "classes")
        target_df_reference = reference.reference.select(
            self.model.target.name
        ).withColumnRenamed(self.model.target.name, "classes")
        prediction_target_df = (
            predictions_df_current.union(target_df_current)
            .union(predictions_df_reference)
            .union(target_df_reference)
        )
        indexer = StringIndexer(
            inputCol="classes",
            outputCol="classes_index",
            stringOrderType="alphabetAsc",
            handleInvalid="skip",
        )
        indexer_model = indexer.fit(prediction_target_df)
        indexer_prediction = indexer_model.setInputCol(
            self.model.outputs.prediction.name
        ).setOutputCol(f"{self.model.outputs.prediction.name}-idx")
        indexed_prediction_df = indexer_prediction.transform(self.current)
        indexer_target = indexer_model.setInputCol(self.model.target.name).setOutputCol(
            f"{self.model.target.name}-idx"
        )
        indexed_target_df = indexer_target.transform(indexed_prediction_df)

        index_label_map = {
            str(float(index)): str(label)
            for index, label in enumerate(indexer_model.labelsArray[0])
        }
        return index_label_map, indexed_target_df
