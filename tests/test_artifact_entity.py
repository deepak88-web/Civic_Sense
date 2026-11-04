
from pathlib import Path

from civicsense.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
    ModelEvaluationArtifact,
    PredictionArtifact
)


# Test Data Ingestion Artifact
ingestion_artifact = DataIngestionArtifact(
    supervised_data_file_path=Path("artifacts/supervised.csv"),
    prediction_data_file_path=Path("artifacts/prediction.csv")
)


# Test Data Validation Artifact
validation_artifact = DataValidationArtifact(
    validation_status=True,
    validation_message="Validation successful",
    validated_supervised_file_path=Path("artifacts/supervised.csv"),
    validated_prediction_file_path=Path("artifacts/prediction.csv")
)


# Test Data Transformation Artifact
transformation_artifact = DataTransformationArtifact(
    transformed_data_file_path=Path("artifacts/tokenized_data.npz"),
    tokenizer_file_path=Path("artifacts/tokenizer.pkl"),
    label_encoder_file_path=Path("artifacts/label_encoder.pkl"),
    max_sequence_length_file_path=Path("artifacts/max_len.npy"),
    embedding_matrix_file_path=Path("artifacts/embedding_matrix.npy"),
    word2vec_model_file_path=Path("artifacts/word2vec.model")
)


# Test Model Trainer Artifact
trainer_artifact = ModelTrainerArtifact(
    trained_model_file_path=Path("artifacts/lstm.keras"),
    training_history_file_path=Path("artifacts/history.csv")
)


# Test Model Evaluation Artifact
evaluation_artifact = ModelEvaluationArtifact(
    evaluation_status=True,
    metrics_file_path=Path("artifacts/metrics.json"),
    classification_report_file_path=Path("artifacts/report.csv"),
    confusion_matrix_file_path=Path("artifacts/confusion_matrix.csv")
)


# Test Prediction Artifact
prediction_artifact = PredictionArtifact(
    predictions_file_path=Path("predictions/batch_predictions.csv"),
    low_confidence_file_path=Path("predictions/low_confidence.csv"),
    prediction_summary_file_path=Path("predictions/summary.csv"),
    total_predictions=27686,
    low_confidence_count=100
)


print("All artifact classes initialized successfully!")

print("\nTotal predictions:",
      prediction_artifact.total_predictions)
