
import sys

from civicsense.logger import get_logger
from civicsense.exception import CivicSenseException

from civicsense.entity.config_entity import (
    DataIngestionConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    BatchPredictionConfig
)

from civicsense.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact
)

from civicsense.components.data_ingestion import DataIngestion
from civicsense.components.batch_prediction import BatchPrediction


logger = get_logger(__name__)


class PredictionPipeline:

    def initiate_prediction_pipeline(self):

        try:
            logger.info("Prediction pipeline started.")

            # Step 1: Data Ingestion
            data_ingestion = DataIngestion(
                data_ingestion_config=DataIngestionConfig()
            )

            ingestion_artifact = (
                data_ingestion.initiate_data_ingestion()
            )

            # Step 2: Reconstruct saved transformation artifact paths
            transformation_config = DataTransformationConfig()

            transformation_artifact = DataTransformationArtifact(
                transformed_data_file_path=(
                    transformation_config.transformed_data_path
                ),
                tokenizer_file_path=(
                    transformation_config.tokenizer_path
                ),
                label_encoder_file_path=(
                    transformation_config.label_encoder_path
                ),
                max_sequence_length_file_path=(
                    transformation_config.max_len_path
                ),
                embedding_matrix_file_path=(
                    transformation_config.embedding_matrix_path
                ),
                word2vec_model_file_path=(
                    transformation_config.word2vec_model_path
                )
            )

            # Step 3: Reconstruct saved model artifact paths
            trainer_config = ModelTrainerConfig()

            trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=trainer_config.model_path,
                training_history_file_path=(
                    trainer_config.training_history_path
                )
            )

            # Step 4: Initialize batch prediction
            batch_prediction = BatchPrediction(
                prediction_config=BatchPredictionConfig(),
                data_ingestion_artifact=ingestion_artifact,
                data_transformation_artifact=transformation_artifact,
                model_trainer_artifact=trainer_artifact
            )

            # Step 5: Run batch prediction
            prediction_artifact = (
                batch_prediction.initiate_prediction()
            )

            logger.info(
                "Prediction pipeline completed successfully."
            )

            return prediction_artifact

        except Exception as e:
            logger.exception(
                "Error occurred in prediction pipeline."
            )
            raise CivicSenseException(e, sys)
