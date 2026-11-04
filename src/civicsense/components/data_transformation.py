
import sys
import pickle
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from gensim.models import Word2Vec

from civicsense.logger import get_logger
from civicsense.exception import CivicSenseException

from civicsense.entity.config_entity import DataTransformationConfig
from civicsense.entity.artifact_entity import (
    DataValidationArtifact,
    DataTransformationArtifact
)

from civicsense.utils.common import create_directories


logger = get_logger(__name__)


class DataTransformation:

    def __init__(
        self,
        data_transformation_config: DataTransformationConfig,
        data_validation_artifact: DataValidationArtifact
    ):
        self.data_transformation_config = data_transformation_config
        self.data_validation_artifact = data_validation_artifact

    def initiate_data_transformation(self) -> DataTransformationArtifact:

        try:
            logger.info("Data transformation started.")

            config = self.data_transformation_config

            create_directories([
                str(config.root_dir),
                str(config.transformed_data_path.parent),
                str(config.tokenizer_path.parent),
                str(config.label_encoder_path.parent),
                str(config.max_len_path.parent),
                str(config.embedding_matrix_path.parent),
                str(config.word2vec_model_path.parent)
            ])

            # 1. Load validated supervised dataset
            supervised_path = (
                self.data_validation_artifact
                .validated_supervised_file_path
            )

            supervised_df = pd.read_csv(supervised_path)

            if supervised_df.empty:
                raise ValueError("Supervised dataset is empty.")

            X = supervised_df["cleaned_text"].astype(str)
            y = supervised_df["target_category"]

            logger.info(f"Loaded supervised dataset: {supervised_df.shape}")

            # 2. Split dataset into train, validation and test sets
            X_train_val, X_test, y_train_val, y_test = train_test_split(
                X,
                y,
                test_size=config.test_size,
                random_state=config.random_state,
                stratify=y
            )

            X_train, X_val, y_train, y_val = train_test_split(
                X_train_val,
                y_train_val,
                test_size=config.validation_size / (1 - config.test_size),
                random_state=config.random_state,
                stratify=y_train_val
            )

            logger.info(
                f"Training samples: {len(X_train)}, "
                f"Validation samples: {len(X_val)}, "
                f"Test samples: {len(X_test)}"
            )

            # 3. Initialize and fit tokenizer on training text only
            tokenizer = Tokenizer(oov_token=config.oov_token)

            tokenizer.fit_on_texts(X_train)

            word_index = tokenizer.word_index

            logger.info(
                f"Tokenizer vocabulary size: {len(word_index)}"
            )

            # 4. Convert text into integer sequences
            train_sequences = tokenizer.texts_to_sequences(X_train)
            val_sequences = tokenizer.texts_to_sequences(X_val)
            test_sequences = tokenizer.texts_to_sequences(X_test)

            # 5. Apply post-padding and post-truncation
            X_train_padded = pad_sequences(
                train_sequences,
                maxlen=config.max_sequence_length,
                padding=config.padding_type,
                truncating=config.truncating_type
            )

            X_val_padded = pad_sequences(
                val_sequences,
                maxlen=config.max_sequence_length,
                padding=config.padding_type,
                truncating=config.truncating_type
            )

            X_test_padded = pad_sequences(
                test_sequences,
                maxlen=config.max_sequence_length,
                padding=config.padding_type,
                truncating=config.truncating_type
            )

            logger.info(
                f"Padded training shape: {X_train_padded.shape}"
            )

            # 6. Encode target categories
            label_encoder = LabelEncoder()

            y_train_encoded = label_encoder.fit_transform(y_train)
            y_val_encoded = label_encoder.transform(y_val)
            y_test_encoded = label_encoder.transform(y_test)

            logger.info(
                f"Number of encoded classes: {len(label_encoder.classes_)}"
            )

            # 7. Prepare training sentences for Word2Vec
            # Padding index 0 is excluded; OOV index is retained.
            index_word = {
                index: word
                for word, index in word_index.items()
            }

            train_sentences = [
                [
                    index_word.get(int(token), config.oov_token)
                    for token in sequence
                    if token != 0
                ]
                for sequence in X_train_padded
            ]

            # 8. Train Word2Vec using training sentences only
            word2vec_model = Word2Vec(
                sentences=train_sentences,
                vector_size=config.embedding_dimension,
                window=config.window_size,
                min_count=config.min_word_count,
                workers=config.workers,
                sg=config.sg,
                epochs=config.word2vec_epochs,
                seed=config.word2vec_seed
            )

            logger.info(
                f"Word2Vec vocabulary size: {len(word2vec_model.wv)}"
            )

            # 9. Create embedding matrix
            vocab_size = len(word_index) + 1

            embedding_matrix = np.zeros(
                (vocab_size, config.embedding_dimension),
                dtype=np.float32
            )

            matched_words = 0

            for word, index in word_index.items():

                if word in word2vec_model.wv:
                    embedding_matrix[index] = word2vec_model.wv[word]
                    matched_words += 1

            embedding_coverage = (
                matched_words / len(word_index) * 100
                if word_index else 0
            )

            logger.info(
                f"Embedding matrix shape: {embedding_matrix.shape}"
            )
            logger.info(
                f"Word2Vec embedding coverage: {embedding_coverage:.2f}%"
            )

            # 10. Save tokenizer and label encoder
            with open(config.tokenizer_path, "wb") as file:
                pickle.dump(tokenizer, file)

            with open(config.label_encoder_path, "wb") as file:
                pickle.dump(label_encoder, file)

            # 11. Save maximum sequence length
            np.save(
                config.max_len_path,
                config.max_sequence_length
            )

            # 12. Save transformed datasets
            np.savez_compressed(
                config.transformed_data_path,
                X_train=X_train_padded,
                X_val=X_val_padded,
                X_test=X_test_padded,
                y_train=y_train_encoded,
                y_val=y_val_encoded,
                y_test=y_test_encoded
            )

            # 13. Save embedding matrix and Word2Vec model
            np.save(
                config.embedding_matrix_path,
                embedding_matrix
            )

            word2vec_model.save(
                str(config.word2vec_model_path)
            )

            logger.info("All transformation artifacts saved successfully.")

            # 14. Create transformation artifact
            transformation_artifact = DataTransformationArtifact(
                transformed_data_file_path=config.transformed_data_path,
                tokenizer_file_path=config.tokenizer_path,
                label_encoder_file_path=config.label_encoder_path,
                max_sequence_length_file_path=config.max_len_path,
                embedding_matrix_file_path=config.embedding_matrix_path,
                word2vec_model_file_path=config.word2vec_model_path
            )

            logger.info("Data transformation completed successfully.")

            return transformation_artifact

        except Exception as e:
            logger.exception("Error occurred during data transformation.")
            raise CivicSenseException(e, sys)
