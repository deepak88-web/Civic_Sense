
import sys
import pandas as pd

from civicsense.logger import get_logger
from civicsense.exception import CivicSenseException

from civicsense.entity.config_entity import DataIngestionConfig
from civicsense.entity.artifact_entity import DataIngestionArtifact

from civicsense.utils.common import create_directories


logger = get_logger(__name__)


class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig):

        self.data_ingestion_config = data_ingestion_config

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Reads the cleaned supervised and prediction datasets
        and stores them in the data ingestion artifact directory.
        """

        try:
            logger.info("Data ingestion started.")

            config = self.data_ingestion_config

            # Create artifact directory
            create_directories([str(config.root_dir)])

            # Check whether input files exist
            if not config.supervised_data_path.is_file():
                raise FileNotFoundError(
                    f"Supervised dataset not found: "
                    f"{config.supervised_data_path}"
                )

            if not config.prediction_data_path.is_file():
                raise FileNotFoundError(
                    f"Prediction dataset not found: "
                    f"{config.prediction_data_path}"
                )

            # Load supervised dataset
            supervised_df = pd.read_csv(
                config.supervised_data_path
            )

            # Load prediction dataset
            prediction_df = pd.read_csv(
                config.prediction_data_path
            )

            # Check for empty datasets
            if supervised_df.empty:
                raise ValueError("Supervised dataset is empty.")

            if prediction_df.empty:
                raise ValueError("Prediction dataset is empty.")

            logger.info(
                f"Supervised dataset loaded: {supervised_df.shape}"
            )

            logger.info(
                f"Prediction dataset loaded: {prediction_df.shape}"
            )

            # Save datasets into artifact directory
            supervised_df.to_csv(
                config.ingested_supervised_path,
                index=False
            )

            prediction_df.to_csv(
                config.ingested_prediction_path,
                index=False
            )

            logger.info("Both datasets saved successfully.")

            # Create ingestion artifact
            data_ingestion_artifact = DataIngestionArtifact(
                supervised_data_file_path=(
                    config.ingested_supervised_path
                ),
                prediction_data_file_path=(
                    config.ingested_prediction_path
                )
            )

            logger.info("Data ingestion completed successfully.")

            return data_ingestion_artifact

        except Exception as e:
            logger.exception("Error occurred during data ingestion.")
            raise CivicSenseException(e, sys)
