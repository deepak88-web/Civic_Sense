
import sys
import pickle
import numpy as np
import pandas as pd
import tensorflow as tf

from tensorflow.keras.preprocessing.sequence import pad_sequences

from civicsense.logger import get_logger
from civicsense.exception import CivicSenseException

from civicsense.entity.config_entity import BatchPredictionConfig

from civicsense.entity.artifact_entity import (
    DataIngestionArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
    BatchPredictionArtifact
)

from civicsense.utils.common import create_directories


logger = get_logger(__name__)


class BatchPrediction:

    def __init__(
        self,
        prediction_config: BatchPredictionConfig,
        data_ingestion_artifact: DataIngestionArtifact,
        data_transformation_artifact: DataTransformationArtifact,
        model_trainer_artifact: ModelTrainerArtifact
    ):
        self.prediction_config = prediction_config
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_artifact = model_trainer_artifact

    def initiate_prediction(self) -> BatchPredictionArtifact:

        try:
            logger.info("Batch prediction started.")

            config = self.prediction_config

            create_directories([
                str(config.root_dir),
                str(config.predictions_file_path.parent),
                str(config.low_confidence_file_path.parent),
                str(config.prediction_summary_path.parent)
            ])

            # 1. Load unseen prediction dataset
            prediction_df = pd.read_csv(
                self.data_ingestion_artifact.prediction_data_file_path
            )

            if prediction_df.empty:
                raise ValueError("Prediction dataset is empty.")

            if "cleaned_text" not in prediction_df.columns:
                raise ValueError(
                    "Prediction dataset must contain cleaned_text."
                )

            if prediction_df["cleaned_text"].isna().any():
                raise ValueError(
                  "Prediction dataset contains missing cleaned_text values."
                )

            logger.info(
                f"Prediction dataset loaded: {prediction_df.shape}"
            )

            # 2. Load trained LSTM model
            model = tf.keras.models.load_model(
                self.model_trainer_artifact.trained_model_file_path
            )

            # 3. Load tokenizer
            with open(
                self.data_transformation_artifact.tokenizer_file_path,
                "rb"
            ) as file:
                tokenizer = pickle.load(file)

            # 4. Load label encoder
            with open(
                self.data_transformation_artifact.label_encoder_file_path,
                "rb"
            ) as file:
                label_encoder = pickle.load(file)

            # 5. Load maximum sequence length
            max_len = int(
                np.load(
                    self.data_transformation_artifact
                    .max_sequence_length_file_path
                )
            )

            logger.info("Model and preprocessing artifacts loaded.")

            # 6. Convert complaint text into sequences
            prediction_texts = (
                prediction_df["cleaned_text"].astype(str).tolist()
            )

            prediction_sequences = tokenizer.texts_to_sequences(
                prediction_texts
            )

            # 7. Apply the same padding used during training
            X_prediction = pad_sequences(
                prediction_sequences,
                maxlen=max_len,
                padding=config.padding_type,
                truncating=config.truncating_type
            )

            logger.info(
                f"Padded prediction shape: {X_prediction.shape}"
            )

            # 8. Generate prediction probabilities
            prediction_probabilities = model.predict(
                X_prediction,
                batch_size=config.batch_size,
                verbose=1
            )

            # 9. Get predicted category and confidence
            predicted_class_indices = np.argmax(
                prediction_probabilities,
                axis=1
            )

            predicted_categories = label_encoder.inverse_transform(
                predicted_class_indices
            )

            confidence_scores = np.max(
                prediction_probabilities,
                axis=1
            )

            # 10. Preserve original dataset columns
            final_predictions = prediction_df.copy()

            final_predictions["predicted_category"] = (
                predicted_categories
            )

            final_predictions["confidence_score"] = confidence_scores

            # 11. Assign confidence levels
            final_predictions["prediction_status"] = np.select(
                [
                    final_predictions["confidence_score"]
                    >= config.high_confidence_threshold,

                    final_predictions["confidence_score"]
                    >= config.medium_confidence_threshold
                ],
                [
                    "High",
                    "Medium"
                ],
                default="Low"
            )

            logger.info("Predictions and confidence levels generated.")

            # 12. Create category-wise summary
            category_counts = (
                final_predictions["predicted_category"]
                .value_counts()
            )

            category_percentages = (
                final_predictions["predicted_category"]
                .value_counts(normalize=True) * 100
            )

            category_summary = pd.DataFrame({
                "Complaint Count": category_counts,
                "Percentage": category_percentages
            })

            category_output = category_summary.reset_index()

            category_output.columns = [
                "Category",
                "Complaint Count",
                "Percentage"
            ]

            category_output["Summary Type"] = (
                "Category Distribution"
            )

            category_output["Confidence Level"] = np.nan

            # 13. Create confidence-wise summary
            confidence_counts = (
                final_predictions["prediction_status"]
                .value_counts()
            )

            confidence_percentages = (
                final_predictions["prediction_status"]
                .value_counts(normalize=True) * 100
            )

            confidence_summary = pd.DataFrame({
                "Complaint Count": confidence_counts,
                "Percentage": confidence_percentages
            })

            confidence_output = confidence_summary.reset_index()

            confidence_output.columns = [
                "Confidence Level",
                "Complaint Count",
                "Percentage"
            ]

            confidence_output["Summary Type"] = (
                "Confidence Distribution"
            )

            confidence_output["Category"] = np.nan

            # 14. Combine both summaries
            prediction_summary = pd.concat(
                [
                    category_output[
                        [
                            "Summary Type",
                            "Category",
                            "Confidence Level",
                            "Complaint Count",
                            "Percentage"
                        ]
                    ],
                    confidence_output[
                        [
                            "Summary Type",
                            "Category",
                            "Confidence Level",
                            "Complaint Count",
                            "Percentage"
                        ]
                    ]
                ],
                ignore_index=True
            )

            # 15. Extract low-confidence complaints
            low_confidence_df = final_predictions[
                final_predictions["prediction_status"] == "Low"
            ].copy()

            # 16. Save all prediction outputs
            final_predictions.to_csv(
                config.predictions_file_path,
                index=False
            )

            low_confidence_df.to_csv(
                config.low_confidence_file_path,
                index=False
            )

            prediction_summary.to_csv(
                config.prediction_summary_path,
                index=False
            )

            logger.info("All prediction files saved successfully.")

            # 17. Create prediction artifact
            prediction_artifact = BatchPredictionArtifact(
                predictions_file_path=config.predictions_file_path,
                low_confidence_file_path=config.low_confidence_file_path,
                prediction_summary_file_path=config.prediction_summary_path,
                total_predictions=len(final_predictions),
                low_confidence_count=len(low_confidence_df)
            )

            logger.info(
                f"Total predictions: {len(final_predictions)}"
            )

            logger.info(
                f"Low-confidence predictions: {len(low_confidence_df)}"
            )

            logger.info("Batch prediction completed successfully.")

            return prediction_artifact

        except Exception as e:
            logger.exception("Error occurred during batch prediction.")
            raise CivicSenseException(e, sys)
