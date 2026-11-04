
import sys

from civicsense.logger import get_logger
from civicsense.exception import CivicSenseException

from civicsense.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    ModelEvaluationConfig
)

from civicsense.components.data_ingestion import DataIngestion
from civicsense.components.data_validation import DataValidation
from civicsense.components.data_transformation import DataTransformation
from civicsense.components.model_trainer import ModelTrainer
from civicsense.components.model_evaluation import ModelEvaluation


logger = get_logger(__name__)


class TrainingPipeline:

    def initiate_training_pipeline(self):

        try:
            logger.info("Training pipeline started.")

            # Step 1: Data Ingestion
            data_ingestion = DataIngestion(
                data_ingestion_config=DataIngestionConfig()
            )

            ingestion_artifact = (
                data_ingestion.initiate_data_ingestion()
            )

            # Step 2: Data Validation
            data_validation = DataValidation(
                data_validation_config=DataValidationConfig(),
                data_ingestion_artifact=ingestion_artifact
            )

            validation_artifact = (
                data_validation.initiate_data_validation()
            )

            if not validation_artifact.validation_status:
                raise ValueError(
                    "Data validation failed. "
                    "Training pipeline cannot continue."
                )

            # Step 3: Data Transformation
            data_transformation = DataTransformation(
                data_transformation_config=DataTransformationConfig(),
                data_validation_artifact=validation_artifact
            )

            transformation_artifact = (
                data_transformation.initiate_data_transformation()
            )

            # Step 4: Model Training
            model_trainer = ModelTrainer(
                model_trainer_config=ModelTrainerConfig(),
                data_transformation_artifact=transformation_artifact
            )

            trainer_artifact = (
                model_trainer.initiate_model_training()
            )

            # Step 5: Model Evaluation
            model_evaluation = ModelEvaluation(
                model_evaluation_config=ModelEvaluationConfig(),
                data_transformation_artifact=transformation_artifact,
                model_trainer_artifact=trainer_artifact
            )

            evaluation_artifact = (
                model_evaluation.initiate_model_evaluation()
            )

            logger.info(
                "Training pipeline completed successfully."
            )

            return evaluation_artifact

        except Exception as e:
            logger.exception(
                "Error occurred in training pipeline."
            )
            raise CivicSenseException(e, sys) from e
