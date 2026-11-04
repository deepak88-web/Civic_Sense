
import sys
import json
import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from civicsense.logger import get_logger
from civicsense.exception import CivicSenseException

from civicsense.entity.config_entity import ModelEvaluationConfig
from civicsense.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact,
    ModelEvaluationArtifact
)

from civicsense.utils.common import create_directories


logger = get_logger(__name__)


class ModelEvaluation:

    def __init__(
        self,
        model_evaluation_config: ModelEvaluationConfig,
        data_transformation_artifact: DataTransformationArtifact,
        model_trainer_artifact: ModelTrainerArtifact
    ):
        self.model_evaluation_config = model_evaluation_config
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_artifact = model_trainer_artifact

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:

        try:
            logger.info("Model evaluation started.")

            config = self.model_evaluation_config

            create_directories([str(config.root_dir)])

            # 1. Load the test dataset
            transformed_data = np.load(
                self.data_transformation_artifact.transformed_data_file_path
            )

            X_test = transformed_data["X_test"]
            y_test = transformed_data["y_test"]

            logger.info(f"Test data shape: {X_test.shape}")

            # 2. Load the trained LSTM model
            model = tf.keras.models.load_model(
                self.model_trainer_artifact.trained_model_file_path
            )

            logger.info("Trained LSTM model loaded successfully.")

            # 3. Load label encoder
            import pickle

            with open(
                self.data_transformation_artifact.label_encoder_file_path,
                "rb"
            ) as file:
                label_encoder = pickle.load(file)

            class_names = label_encoder.classes_

            # 4. Generate test predictions
            y_test_prob = model.predict(X_test, verbose=0)

            y_test_pred = np.argmax(y_test_prob, axis=1)

            # 5. Calculate overall evaluation metrics
            metrics = {
                "Test Accuracy": float(
                    accuracy_score(y_test, y_test_pred)
                ),
                "Macro Precision": float(
                    precision_score(
                        y_test, y_test_pred,
                        average="macro",
                        zero_division=0
                    )
                ),
                "Macro Recall": float(
                    recall_score(
                        y_test, y_test_pred,
                        average="macro",
                        zero_division=0
                    )
                ),
                "Macro F1-score": float(
                    f1_score(
                        y_test, y_test_pred,
                        average="macro",
                        zero_division=0
                    )
                ),
                "Weighted F1-score": float(
                    f1_score(
                        y_test, y_test_pred,
                        average="weighted",
                        zero_division=0
                    )
                )
            }

            logger.info(f"Test evaluation metrics: {metrics}")

            # 6. Generate classification report
            report = classification_report(
                y_test,
                y_test_pred,
                labels=np.arange(len(class_names)),
                target_names=class_names,
                output_dict=True,
                zero_division=0
            )

            report_df = pd.DataFrame(report).transpose()

            # 7. Generate confusion matrix
            cm = confusion_matrix(
                y_test,
                y_test_pred,
                labels=np.arange(len(class_names))
            )

            cm_df = pd.DataFrame(
                cm,
                index=class_names,
                columns=class_names
            )

            # 8. Save evaluation metrics
            with open(
                config.metrics_file_path,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(metrics, file, indent=4)

            # 9. Save classification report
            report_df.to_csv(
                config.classification_report_path
            )

            # 10. Save confusion matrix
            cm_df.to_csv(
                config.confusion_matrix_path
            )

            logger.info("All evaluation results saved successfully.")

            # 11. Create evaluation artifact
            evaluation_artifact = ModelEvaluationArtifact(
                evaluation_status=True,
                metrics_file_path=config.metrics_file_path,
                classification_report_file_path=(
                    config.classification_report_path
                ),
                confusion_matrix_file_path=(
                    config.confusion_matrix_path
                )
            )

            logger.info("Model evaluation completed successfully.")

            return evaluation_artifact

        except Exception as e:
            logger.exception("Error occurred during model evaluation.")
            raise CivicSenseException(e, sys)
