
import sys
import pandas as pd

from civicsense.logger import get_logger
from civicsense.exception import CivicSenseException

from civicsense.entity.config_entity import DataValidationConfig
from civicsense.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact
)

from civicsense.utils.common import create_directories

logger = get_logger(__name__)


class DataValidation:

    def __init__(
        self,
        data_validation_config: DataValidationConfig,
        data_ingestion_artifact: DataIngestionArtifact
    ):
        self.data_validation_config = data_validation_config
        self.data_ingestion_artifact = data_ingestion_artifact

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logger.info("Data validation started.")

            config = self.data_validation_config

            create_directories([
                str(config.root_dir),
                str(config.status_file_path.parent)
            ])

            supervised_path = (
                self.data_ingestion_artifact.supervised_data_file_path
            )
            prediction_path = (
                self.data_ingestion_artifact.prediction_data_file_path
            )

            # Check whether both files exist
            if not supervised_path.is_file():
                raise FileNotFoundError(
                    f"Supervised file not found: {supervised_path}"
                )

            if not prediction_path.is_file():
                raise FileNotFoundError(
                    f"Prediction file not found: {prediction_path}"
                )

            # Load datasets
            supervised_df = pd.read_csv(supervised_path)
            prediction_df = pd.read_csv(prediction_path)

            if supervised_df.empty:
                raise ValueError("Supervised dataset is empty.")

            if prediction_df.empty:
                raise ValueError("Prediction dataset is empty.")

            logger.info(
                f"Supervised dataset shape: {supervised_df.shape}"
            )
            logger.info(
                f"Prediction dataset shape: {prediction_df.shape}"
            )

            # Validate required columns
            missing_supervised = set(
                config.required_supervised_columns
            ) - set(supervised_df.columns)

            missing_prediction = set(
                config.required_prediction_columns
            ) - set(prediction_df.columns)

            if missing_supervised:
                raise ValueError(
                    f"Missing supervised columns: {missing_supervised}"
                )

            if missing_prediction:
                raise ValueError(
                    f"Missing prediction columns: {missing_prediction}"
                )

            # Validate missing and blank values
            for column in config.required_supervised_columns:
                if supervised_df[column].isna().any():
                    raise ValueError(
                        f"Missing values found in supervised column: {column}"
                    )

                if supervised_df[column].astype(str).str.strip().eq("").any():
                    raise ValueError(
                        f"Blank values found in supervised column: {column}"
                    )

            for column in config.required_prediction_columns:
                if prediction_df[column].isna().any():
                    raise ValueError(
                        f"Missing values found in prediction column: {column}"
                    )

                if prediction_df[column].astype(str).str.strip().eq("").any():
                    raise ValueError(
                        f"Blank values found in prediction column: {column}"
                    )

            # Validate target categories
            actual_categories = set(
                supervised_df["target_category"].unique()
            )

            if len(actual_categories) != config.expected_num_classes:
                raise ValueError(
                    f"Expected {config.expected_num_classes} categories, "
                    f"but found {len(actual_categories)}."
                )

            logger.info(
                f"Found {len(actual_categories)} target categories."
            )

            # Save validation status
            validation_message = "Both datasets passed validation."

            config.status_file_path.write_text(
                validation_message,
                encoding="utf-8"
            )

            artifact = DataValidationArtifact(
                validation_status=True,
                validation_message=validation_message,
                validated_supervised_file_path=supervised_path,
                validated_prediction_file_path=prediction_path
            )

            logger.info("Data validation completed successfully.")

            return artifact

        except Exception as e:
            logger.exception("Error occurred during data validation.")

            config = self.data_validation_config
            create_directories([str(config.root_dir)])

            config.status_file_path.write_text(
                f"Validation failed: {str(e)}",
                encoding="utf-8"
            )

            raise CivicSenseException(e, sys)
