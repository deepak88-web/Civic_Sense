
from dataclasses import dataclass, field
from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[3]


@dataclass
class DataIngestionConfig:

    root_dir: Path = field(
        default_factory=lambda: PROJECT_ROOT / "artifacts/data_ingestion"
    )

    supervised_data_path: Path = field(
        default_factory=lambda: PROJECT_ROOT / "data/interim/civicsense_supervised_cleaned.csv"
    )

    prediction_data_path: Path = field(
        default_factory=lambda: PROJECT_ROOT / "data/interim/civicsense_prediction_cleaned.csv"
    )

    ingested_supervised_path: Path = field(
        default_factory=lambda: PROJECT_ROOT / "artifacts/data_ingestion/supervised.csv"
    )

    ingested_prediction_path: Path = field(
        default_factory=lambda: PROJECT_ROOT / "artifacts/data_ingestion/prediction.csv"
    )


@dataclass
class DataValidationConfig:

    root_dir: Path = field(
        default_factory=lambda: PROJECT_ROOT / "artifacts/data_validation"
    )

    status_file_path: Path = field(
        default_factory=lambda: PROJECT_ROOT / "artifacts/data_validation/status.txt"
    )

    required_supervised_columns = (
        "cleaned_text",
        "target_category",
        "source_dataset"
    )

    required_prediction_columns: tuple = (
        "cleaned_text",
        "detectedLanguage"
    )

    expected_num_classes: int = 12


@dataclass
class DataTransformationConfig:

    root_dir: Path = field(
        default_factory=lambda: PROJECT_ROOT / "artifacts/data_transformation"
    )

    transformed_data_path: Path = field(
        default_factory=lambda: PROJECT_ROOT / "artifacts/data_transformation/tokenized_data.npz"
    )

    tokenizer_path: Path = field(
        default_factory=lambda: PROJECT_ROOT / "artifacts/data_transformation/tokenizer.pkl"
    )

    label_encoder_path: Path = field(
        default_factory=lambda: PROJECT_ROOT / "artifacts/data_transformation/label_encoder.pkl"
    )

    max_len_path: Path = field(
        default_factory=lambda: PROJECT_ROOT / "artifacts/data_transformation/max_len.npy"
    )

    embedding_matrix_path: Path = field(
        default_factory=lambda: PROJECT_ROOT / "artifacts/data_transformation/word2vec_embedding_matrix.npy"
    )

    word2vec_model_path: Path = field(
        default_factory=lambda: PROJECT_ROOT
        / "artifacts/data_transformation/civicsense_word2vec.model"
    )

    # Data splitting configuration
    test_size: float = 0.15
    validation_size: float = 0.15
    random_state: int = 42

    # Tokenization configuration
    max_sequence_length: int = 156
    oov_token: str = "<OOV>"
    padding_type: str = "post"
    truncating_type: str = "post"

    # Word2Vec configuration
    embedding_dimension: int = 100
    window_size: int = 5
    min_word_count: int = 2
    workers: int = 4
    sg: int = 1
    word2vec_epochs: int = 10
    word2vec_seed: int = 42


@dataclass
class ModelTrainerConfig:

    root_dir: Path = field(
        default_factory=lambda: PROJECT_ROOT / "artifacts/model_trainer"
    )

    model_path: Path = field(
        default_factory=lambda: PROJECT_ROOT / "artifacts/model_trainer/lstm_word2vec.keras"
    )

    training_history_path: Path = field(
        default_factory=lambda: PROJECT_ROOT / "artifacts/model_trainer/training_history.csv"
    )

    # LSTM architecture
    lstm_units: int = 64
    dropout_rate: float = 0.3

    # Training configuration
    epochs: int = 15
    batch_size: int = 64
    optimizer: str = "adam"
    loss: str = "sparse_categorical_crossentropy"

    # Early stopping
    early_stopping_monitor: str = "val_loss"
    early_stopping_patience: int = 3
    restore_best_weights: bool = True

    random_seed: int = 42


@dataclass
class ModelEvaluationConfig:

    root_dir: Path = field(
        default_factory=lambda: PROJECT_ROOT / "artifacts/model_evaluation"
    )

    metrics_file_path: Path = field(
        default_factory=lambda: PROJECT_ROOT / "artifacts/model_evaluation/test_metrics.json"
    )

    classification_report_path: Path = field(
        default_factory=lambda: PROJECT_ROOT / "artifacts/model_evaluation/classification_report.csv"
    )

    confusion_matrix_path: Path = field(
        default_factory=lambda: PROJECT_ROOT / "artifacts/model_evaluation/confusion_matrix.csv"
    )



@dataclass
class BatchPredictionConfig:

    root_dir: Path = field(
        default_factory=lambda: PROJECT_ROOT / "artifacts/prediction"
    )

    predictions_file_path: Path = field(
        default_factory=lambda: PROJECT_ROOT
        / "artifacts/prediction/civicsense_batch_predictions.csv"
    )

    low_confidence_file_path: Path = field(
        default_factory=lambda: PROJECT_ROOT
        / "artifacts/prediction/civicsense_low_confidence_review.csv"
    )

    prediction_summary_path: Path = field(
        default_factory=lambda: PROJECT_ROOT
        / "artifacts/prediction/prediction_summary.csv"
    )

    batch_size: int = 64

    high_confidence_threshold: float = 0.80
    medium_confidence_threshold: float = 0.60

