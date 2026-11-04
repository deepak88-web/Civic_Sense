
import pandas as pd

from civicsense.components.data_ingestion import DataIngestion
from civicsense.components.batch_prediction import BatchPrediction

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


# Step 1: Run data ingestion to obtain the prediction dataset
ingestion = DataIngestion(
    data_ingestion_config=DataIngestionConfig()
)

ingestion_artifact = ingestion.initiate_data_ingestion()


# Step 2: Create transformation artifact
transformation_config = DataTransformationConfig()

transformation_artifact = DataTransformationArtifact(
    transformed_data_file_path=transformation_config.transformed_data_path,
    tokenizer_file_path=transformation_config.tokenizer_path,
    label_encoder_file_path=transformation_config.label_encoder_path,
    max_sequence_length_file_path=transformation_config.max_len_path,
    embedding_matrix_file_path=transformation_config.embedding_matrix_path,
    word2vec_model_file_path=transformation_config.word2vec_model_path
)


# Step 3: Create trained model artifact
trainer_config = ModelTrainerConfig()

trainer_artifact = ModelTrainerArtifact(
    trained_model_file_path=trainer_config.model_path,
    training_history_file_path=trainer_config.training_history_path
)


# Step 4: Initialize batch prediction 
batch_prediction = BatchPrediction(
    prediction_config=BatchPredictionConfig(),
    data_ingestion_artifact=ingestion_artifact,
    data_transformation_artifact=transformation_artifact,
    model_trainer_artifact=trainer_artifact
)


# Step 5: Run batch prediction
prediction_artifact = batch_prediction.initiate_prediction()


# Step 6: Load and inspect results
predictions = pd.read_csv(
    prediction_artifact.predictions_file_path
)

summary = pd.read_csv(
    prediction_artifact.prediction_summary_file_path
)

print("\nBATCH PREDICTION RESULTS")
print("--------------------------------")

print("Total predictions:", len(predictions))
print("Low-confidence complaints:",
      prediction_artifact.low_confidence_count)

print("\nConfidence distribution:")
print(predictions["prediction_status"].value_counts())

print("\nPredicted category distribution:")
print(predictions["predicted_category"].value_counts())


# Step 7: Verify results
assert len(predictions) == prediction_artifact.total_predictions

assert "predicted_category" in predictions.columns
assert "confidence_score" in predictions.columns
assert "prediction_status" in predictions.columns

assert predictions["predicted_category"].notna().all()
assert predictions["confidence_score"].between(0, 1).all()

assert set(predictions["prediction_status"].unique()).issubset(
    {"High", "Medium", "Low"}
)

assert len(summary) > 0

assert prediction_artifact.predictions_file_path.exists()
assert prediction_artifact.low_confidence_file_path.exists()
assert prediction_artifact.prediction_summary_file_path.exists()

print("\nBatch Prediction Test Successful!")
print("All prediction files have been generated.")
