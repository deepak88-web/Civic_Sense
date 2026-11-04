
import pickle
import logging

import numpy as np
import tensorflow as tf

from tensorflow.keras.preprocessing.sequence import pad_sequences

from civicsense.entity.config_entity import (
    DataTransformationConfig,
    ModelTrainerConfig,
    BatchPredictionConfig
)

from civicsense.utils.text_utils import clean_text


logger = logging.getLogger(__name__)


class PredictionService:
    """
    Service responsible for loading the trained CivicSense model
    and generating predictions for individual complaints.
    """

    def __init__(self):

        self.model = None
        self.tokenizer = None
        self.label_encoder = None
        self.max_sequence_length = None

        self.transformation_config = DataTransformationConfig()
        self.model_config = ModelTrainerConfig()
        self.prediction_config = BatchPredictionConfig()

    def load_artifacts(self):
        """
        Load the trained model and preprocessing artifacts.
        Artifacts are loaded only once per service instance.
        """

        if self.model is not None:
            return

        logger.info("Loading CivicSense model artifacts.")

        required_paths = [
            self.model_config.model_path,
            self.transformation_config.tokenizer_path,
            self.transformation_config.label_encoder_path,
            self.transformation_config.max_len_path
        ]

        for path in required_paths:
            if not path.is_file():
                raise FileNotFoundError(
                    f"Required model artifact not found: {path}. "
                    "Please train the model first."
                )

        # Load trained LSTM model
        self.model = tf.keras.models.load_model(
            self.model_config.model_path
        )

        # Load saved tokenizer
        with open(
            self.transformation_config.tokenizer_path, "rb"
        ) as file:
            self.tokenizer = pickle.load(file)

        # Load saved label encoder
        with open(
            self.transformation_config.label_encoder_path, "rb"
        ) as file:
            self.label_encoder = pickle.load(file)

        # Load maximum sequence length
        self.max_sequence_length = int(
            np.load(self.transformation_config.max_len_path)
        )

        logger.info("CivicSense model artifacts loaded successfully.")

    def predict_complaint(self, complaint_text: str) -> dict:
        """
        Predict the category of a single civic complaint.
        """

        try:

            # 1. Clean complaint text
            cleaned_text = clean_text(complaint_text)

            if not cleaned_text:
                raise ValueError(
                    "Complaint text cannot be empty."
                )

            # 2. Load artifacts if not already loaded
            self.load_artifacts()

            # 3. Convert text into integer sequence
            sequence = self.tokenizer.texts_to_sequences(
                [cleaned_text]
            )

            # 4. Apply the same padding used during training
            padded_sequence = pad_sequences(
                sequence,
                maxlen=self.max_sequence_length,
                padding=self.prediction_config.padding_type,
                truncating=self.prediction_config.truncating_type
            )

            # 5. Generate prediction probabilities
            probabilities = self.model.predict(
                padded_sequence,
                verbose=0
            )

            # 6. Identify predicted category
            predicted_index = int(
                np.argmax(probabilities[0])
            )

            predicted_category = self.label_encoder.inverse_transform(
                [predicted_index]
            )[0]

            # 7. Calculate confidence score
            confidence_score = float(
                np.max(probabilities[0])
            )

            # 8. Determine confidence status
            if confidence_score >= self.prediction_config.high_confidence_threshold:
                prediction_status = "High"

            elif confidence_score >= self.prediction_config.medium_confidence_threshold:
                prediction_status = "Medium"

            else:
                prediction_status = "Low"

            logger.info(
                f"Complaint predicted successfully: "
                f"{predicted_category}, "
                f"confidence={confidence_score:.4f}"
            )

            # 9. Return prediction result
            return {
                "complaint_text": complaint_text,
                "predicted_category": str(predicted_category),
                "confidence_score": confidence_score,
                "prediction_status": prediction_status
            }

        except Exception:
            logger.exception(
                "Error occurred during individual complaint prediction."
            )
            raise


    
    def predict_batch(self, complaint_texts: list[str]) -> list[dict]:
        """
        Generate predictions for multiple civic complaints.
        Reuses the already-loaded model and preprocessing artifacts.
        """

        try:
            if not complaint_texts:
                raise ValueError("No complaints were provided.")

            # 1. Clean all complaint texts
            cleaned_texts = [
                clean_text(text) for text in complaint_texts
            ]

            # 2. Validate complaint texts
            for index, text in enumerate(cleaned_texts):
                if not text:
                    raise ValueError(
                        f"Complaint at row {index + 1} is empty."
                    )

            # 3. Load artifacts if not already loaded
            self.load_artifacts()

            # 4. Convert complaints into sequences
            sequences = self.tokenizer.texts_to_sequences(
                cleaned_texts
            )

            # 5. Apply the same padding used during training
            padded_sequences = pad_sequences(
                sequences,
                maxlen=self.max_sequence_length,
                padding=self.prediction_config.padding_type,
                truncating=self.prediction_config.truncating_type
            )

            # 6. Generate prediction probabilities
            probabilities = self.model.predict(
                padded_sequences,
                batch_size=self.prediction_config.batch_size,
                verbose=0
            )

            # 7. Identify predicted categories
            predicted_indices = np.argmax(
                probabilities,
                axis=1
            )

            predicted_categories = (
                self.label_encoder.inverse_transform(
                    predicted_indices
                )
            )

            # 8. Calculate confidence scores
            confidence_scores = np.max(
                probabilities,
                axis=1
            )

            # 9. Generate prediction results
            results = []

            for original_text, category, confidence in zip(
                complaint_texts,
                predicted_categories,
                confidence_scores
            ):

                confidence = float(confidence)

                if confidence >= self.prediction_config.high_confidence_threshold:
                    status = "High"

                elif confidence >= self.prediction_config.medium_confidence_threshold:
                    status = "Medium"

                else:
                    status = "Low"

                results.append({
                    "complaint_text": original_text,
                    "predicted_category": str(category),
                    "confidence_score": confidence,
                    "prediction_status": status
                })

            logger.info(
                f"Batch prediction completed for {len(results)} complaints."
            )

            return results

        except Exception:
            logger.exception(
                "Error occurred during batch prediction."
            )
            raise
