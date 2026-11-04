
import pickle
import numpy as np

from civicsense.models.lstm import build_lstm_model
from civicsense.entity.config_entity import (
    DataTransformationConfig,
    ModelTrainerConfig
)


# Load transformation configuration
transformation_config = DataTransformationConfig()
trainer_config = ModelTrainerConfig()


# Load embedding matrix
embedding_matrix = np.load(
    transformation_config.embedding_matrix_path
)


# Load label encoder
with open(
    transformation_config.label_encoder_path,
    "rb"
) as file:
    label_encoder = pickle.load(file)


num_classes = len(label_encoder.classes_)


# Build LSTM model
model = build_lstm_model(
    embedding_matrix=embedding_matrix,
    num_classes=num_classes,
    max_sequence_length=transformation_config.max_sequence_length,
    lstm_units=trainer_config.lstm_units,
    dropout_rate=trainer_config.dropout_rate
)


# Display architecture
model.summary()


# Verify architecture
assert model.input_shape == (
    None,
    transformation_config.max_sequence_length
)

assert model.output_shape == (None, num_classes)

assert len(model.layers) == 4

print("\nLSTM Architecture Test Successful!")
print("Input Shape:", model.input_shape)
print("Output Shape:", model.output_shape)
print("Number of Classes:", num_classes)
