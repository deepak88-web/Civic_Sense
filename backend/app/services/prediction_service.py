
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
