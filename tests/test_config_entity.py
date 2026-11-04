
from civicsense.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    ModelEvaluationConfig,
    BatchPredictionConfig
)


# Initialize all configuration objects
ingestion_config = DataIngestionConfig()
validation_config = DataValidationConfig()
transformation_config = DataTransformationConfig()
trainer_config = ModelTrainerConfig()
evaluation_config = ModelEvaluationConfig()
prediction_config = BatchPredictionConfig()


print("\nCONFIGURATION ENTITY TEST")
print("-------------------------")

# Data Ingestion
print("\nData Ingestion:")
print("Supervised dataset:", ingestion_config.supervised_data_path)
print("Prediction dataset:", ingestion_config.prediction_data_path)

# Data Validation
print("\nData Validation:")
print("Expected classes:", validation_config.expected_num_classes)
print("Required supervised columns:",
      validation_config.required_supervised_columns)

# Data Transformation
print("\nData Transformation:")
print("Maximum sequence length:",
      transformation_config.max_sequence_length)
print("Embedding dimension:",
      transformation_config.embedding_dimension)
print("Word2Vec epochs:", transformation_config.word2vec_epochs)

# Model Trainer
print("\nModel Trainer:")
print("LSTM units:", trainer_config.lstm_units)
print("Dropout:", trainer_config.dropout_rate)
print("Epochs:", trainer_config.epochs)
print("Batch size:", trainer_config.batch_size)

# Model Evaluation
print("\nModel Evaluation:")
print("Metrics path:", evaluation_config.metrics_file_path)

# Batch Prediction
print("\nBatch Prediction:")
print("Batch size:", prediction_config.batch_size)
print("High confidence threshold:",
      prediction_config.high_confidence_threshold)
print("Medium confidence threshold:",
      prediction_config.medium_confidence_threshold)


# Verify important values
assert validation_config.expected_num_classes == 12

assert transformation_config.max_sequence_length == 156
assert transformation_config.embedding_dimension == 100
assert transformation_config.word2vec_epochs == 10

assert trainer_config.lstm_units == 64
assert trainer_config.dropout_rate == 0.3
assert trainer_config.epochs == 15
assert trainer_config.batch_size == 64

assert prediction_config.high_confidence_threshold == 0.80
assert prediction_config.medium_confidence_threshold == 0.60

# Verify paths are absolute
assert ingestion_config.supervised_data_path.is_absolute()
assert trainer_config.model_path.is_absolute()
assert prediction_config.predictions_file_path.is_absolute()

print("\nConfiguration Entity Test Successful!")
