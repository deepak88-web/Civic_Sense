
import sys
import numpy as np
import pandas as pd
import tensorflow as tf

from tensorflow.keras.callbacks import EarlyStopping

from civicsense.logger import get_logger
from civicsense.exception import CivicSenseException

from civicsense.models.lstm import build_lstm_model

from civicsense.entity.config_entity import ModelTrainerConfig
from civicsense.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact
)

from civicsense.utils.common import create_directories


logger = get_logger(__name__)


class ModelTrainer:

    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
        data_transformation_artifact: DataTransformationArtifact
    ):
        self.model_trainer_config = model_trainer_config
        self.data_transformation_artifact = data_transformation_artifact

    def initiate_model_training(self) -> ModelTrainerArtifact:

        try:
            logger.info("Model training started.")

            config = self.model_trainer_config

            create_directories([str(config.root_dir)])

            # 1. Load transformed datasets
            transformed_data = np.load(
                self.data_transformation_artifact.transformed_data_file_path
            )

            X_train = transformed_data["X_train"]
            y_train = transformed_data["y_train"]

            X_val = transformed_data["X_val"]
            y_val = transformed_data["y_val"]

            logger.info(f"Training data shape: {X_train.shape}")
            logger.info(f"Validation data shape: {X_val.shape}")

            # 2. Load Word2Vec embedding matrix
            embedding_matrix = np.load(
                self.data_transformation_artifact.embedding_matrix_file_path
            )

            logger.info(
                f"Embedding matrix shape: {embedding_matrix.shape}"
            )

            # 3. Determine number of output classes
            import pickle

            with open(
                self.data_transformation_artifact.label_encoder_file_path,
                "rb"
            ) as file:
                label_encoder = pickle.load(file)

            num_classes = len(label_encoder.classes_)

            logger.info(f"Number of output classes: {num_classes}")

            # 4. Set random seed
            tf.keras.utils.set_random_seed(config.random_seed)

            # 5. Build the LSTM model
            model = build_lstm_model(
                embedding_matrix=embedding_matrix,
                num_classes=num_classes,
                max_sequence_length=X_train.shape[1],
                lstm_units=config.lstm_units,
                dropout_rate=config.dropout_rate
            )

            logger.info("LSTM model architecture created.")

            # 6. Configure early stopping
            early_stopping = EarlyStopping(
                monitor=config.early_stopping_monitor,
                patience=config.early_stopping_patience,
                restore_best_weights=config.restore_best_weights
            )

            # 7. Train the model
            history = model.fit(
                X_train,
                y_train,
                validation_data=(X_val, y_val),
                epochs=config.epochs,
                batch_size=config.batch_size,
                callbacks=[early_stopping],
                verbose=1
            )

            logger.info("Model training completed.")

            # 8. Save trained model
            model.save(config.model_path)

            logger.info(
                f"Trained model saved at: {config.model_path}"
            )

            # 9. Save training history
            history_df = pd.DataFrame(history.history)

            history_df.to_csv(
                config.training_history_path,
                index=False
            )

            logger.info(
                f"Training history saved at: {config.training_history_path}"
            )

            # 10. Create model trainer artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=config.model_path,
                training_history_file_path=config.training_history_path
            )

            logger.info("Model trainer completed successfully.")

            return model_trainer_artifact

        except Exception as e:
            logger.exception("Error occurred during model training.")
            raise CivicSenseException(e, sys)
