
from dataclasses import dataclass, field
from pathlib import Path

from civicsense.entity.config_manager import ConfigurationManager


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[3]


# Load YAML configurations
config_manager = ConfigurationManager()

DATA_CONFIG = config_manager.get_data_config()
MODEL_CONFIG = config_manager.get_model_config()
TRAINING_CONFIG = config_manager.get_training_config()


# Helper function to resolve relative paths
def resolve_path(path_value: str) -> Path:

    path = Path(path_value)

    if path.is_absolute():
        return path

    return PROJECT_ROOT / path


# ==========================================
# DATA INGESTION CONFIGURATION
# ==========================================

@dataclass
class DataIngestionConfig:

    root_dir: Path = field(
        default_factory=lambda: resolve_path(
            DATA_CONFIG["data_ingestion"]["root_dir"]
        )
    )

    supervised_data_path: Path = field(
        default_factory=lambda: resolve_path(
            DATA_CONFIG["data_ingestion"]["supervised_data_path"]
        )
    )

    prediction_data_path: Path = field(
        default_factory=lambda: resolve_path(
            DATA_CONFIG["data_ingestion"]["prediction_data_path"]
        )
    )

    ingested_supervised_path: Path = field(
        default_factory=lambda: resolve_path(
            DATA_CONFIG["data_ingestion"]["ingested_supervised_path"]
        )
    )

    ingested_prediction_path: Path = field(
        default_factory=lambda: resolve_path(
            DATA_CONFIG["data_ingestion"]["ingested_prediction_path"]
        )
    )


# ==========================================
# DATA VALIDATION CONFIGURATION
# ==========================================

@dataclass
class DataValidationConfig:

    root_dir: Path = field(
        default_factory=lambda: resolve_path(
            DATA_CONFIG["data_validation"]["root_dir"]
        )
    )

    status_file_path: Path = field(
        default_factory=lambda: resolve_path(
            DATA_CONFIG["data_validation"]["status_file_path"]
        )
    )

    required_supervised_columns: tuple = field(
        default_factory=lambda: tuple(
            DATA_CONFIG["data_validation"]["required_supervised_columns"]
        )
    )

    required_prediction_columns: tuple = field(
        default_factory=lambda: tuple(
            DATA_CONFIG["data_validation"]["required_prediction_columns"]
        )
    )

    expected_num_classes: int = field(
        default_factory=lambda: DATA_CONFIG[
            "data_validation"
        ]["expected_num_classes"]
    )


# ==========================================
# DATA TRANSFORMATION CONFIGURATION
# ==========================================

@dataclass
class DataTransformationConfig:

    root_dir: Path = field(
        default_factory=lambda: resolve_path(
            DATA_CONFIG["data_transformation"]["root_dir"]
        )
    )

    transformed_data_path: Path = field(
        default_factory=lambda: resolve_path(
            DATA_CONFIG["data_transformation"]["transformed_data_path"]
        )
    )

    tokenizer_path: Path = field(
        default_factory=lambda: resolve_path(
            DATA_CONFIG["data_transformation"]["tokenizer_path"]
        )
    )

    label_encoder_path: Path = field(
        default_factory=lambda: resolve_path(
            DATA_CONFIG["data_transformation"]["label_encoder_path"]
        )
    )

    max_len_path: Path = field(
        default_factory=lambda: resolve_path(
            DATA_CONFIG["data_transformation"]["max_len_path"]
        )
    )

    embedding_matrix_path: Path = field(
        default_factory=lambda: resolve_path(
            DATA_CONFIG["data_transformation"]["embedding_matrix_path"]
        )
    )

    word2vec_model_path: Path = field(
        default_factory=lambda: resolve_path(
            DATA_CONFIG["data_transformation"]["word2vec_model_path"]
        )
    )

    # Data splitting
    test_size: float = field(
        default_factory=lambda: DATA_CONFIG[
            "data_transformation"
        ]["test_size"]
    )

    validation_size: float = field(
        default_factory=lambda: DATA_CONFIG[
            "data_transformation"
        ]["validation_size"]
    )

    random_state: int = field(
        default_factory=lambda: DATA_CONFIG[
            "data_transformation"
        ]["random_state"]
    )

    # Tokenization
    max_sequence_length: int = field(
        default_factory=lambda: DATA_CONFIG[
            "data_transformation"
        ]["max_sequence_length"]
    )

    oov_token: str = field(
        default_factory=lambda: DATA_CONFIG[
            "data_transformation"
        ]["oov_token"]
    )

    padding_type: str = field(
        default_factory=lambda: DATA_CONFIG[
            "data_transformation"
        ]["padding_type"]
    )

    truncating_type: str = field(
        default_factory=lambda: DATA_CONFIG[
            "data_transformation"
        ]["truncating_type"]
    )

    # Word2Vec
    embedding_dimension: int = field(
        default_factory=lambda: DATA_CONFIG[
            "data_transformation"
        ]["embedding_dimension"]
    )

    window_size: int = field(
        default_factory=lambda: DATA_CONFIG[
            "data_transformation"
        ]["window_size"]
    )

    min_word_count: int = field(
        default_factory=lambda: DATA_CONFIG[
            "data_transformation"
        ]["min_word_count"]
    )

    workers: int = field(
        default_factory=lambda: DATA_CONFIG[
            "data_transformation"
        ]["workers"]
    )

    sg: int = field(
        default_factory=lambda: DATA_CONFIG[
            "data_transformation"
        ]["sg"]
    )

    word2vec_epochs: int = field(
        default_factory=lambda: DATA_CONFIG[
            "data_transformation"
        ]["word2vec_epochs"]
    )

    word2vec_seed: int = field(
        default_factory=lambda: DATA_CONFIG[
            "data_transformation"
        ]["word2vec_seed"]
    )


# ==========================================
# MODEL TRAINER CONFIGURATION
# ==========================================

@dataclass
class ModelTrainerConfig:

    root_dir: Path = field(
        default_factory=lambda: resolve_path(
            TRAINING_CONFIG["training"]["root_dir"]
        )
    )

    model_path: Path = field(
        default_factory=lambda: resolve_path(
            MODEL_CONFIG["model"]["model_path"]
        )
    )

    training_history_path: Path = field(
        default_factory=lambda: resolve_path(
            TRAINING_CONFIG["training"]["training_history_path"]
        )
    )

    # LSTM architecture
    lstm_units: int = field(
        default_factory=lambda: MODEL_CONFIG["model"]["lstm_units"]
    )

    dropout_rate: float = field(
        default_factory=lambda: MODEL_CONFIG["model"]["dropout_rate"]
    )

    embedding_trainable: bool = field(
        default_factory=lambda: MODEL_CONFIG["model"]["embedding_trainable"]
    )

    mask_zero: bool = field(
        default_factory=lambda: MODEL_CONFIG["model"]["mask_zero"]
    )

    output_activation: str = field(
        default_factory=lambda: MODEL_CONFIG["model"]["output_activation"]
    )

    # Training parameters
    epochs: int = field(
        default_factory=lambda: TRAINING_CONFIG["training"]["epochs"]
    )

    batch_size: int = field(
        default_factory=lambda: TRAINING_CONFIG["training"]["batch_size"]
    )

    optimizer: str = field(
        default_factory=lambda: TRAINING_CONFIG["training"]["optimizer"]
    )

    loss: str = field(
        default_factory=lambda: TRAINING_CONFIG["training"]["loss"]
    )

    # Early stopping
    early_stopping_monitor: str = field(
        default_factory=lambda: TRAINING_CONFIG[
            "training"
        ]["early_stopping"]["monitor"]
    )

    early_stopping_patience: int = field(
        default_factory=lambda: TRAINING_CONFIG[
            "training"
        ]["early_stopping"]["patience"]
    )

    restore_best_weights: bool = field(
        default_factory=lambda: TRAINING_CONFIG[
            "training"
        ]["early_stopping"]["restore_best_weights"]
    )

    random_seed: int = field(
        default_factory=lambda: TRAINING_CONFIG[
            "training"
        ]["random_seed"]
    )


# ==========================================
# MODEL EVALUATION CONFIGURATION
# ==========================================

@dataclass
class ModelEvaluationConfig:

    root_dir: Path = field(
        default_factory=lambda: resolve_path(
            TRAINING_CONFIG["evaluation"]["root_dir"]
        )
    )

    metrics_file_path: Path = field(
        default_factory=lambda: resolve_path(
            TRAINING_CONFIG["evaluation"]["metrics_file_path"]
        )
    )

    classification_report_path: Path = field(
        default_factory=lambda: resolve_path(
            TRAINING_CONFIG["evaluation"]["classification_report_path"]
        )
    )

    confusion_matrix_path: Path = field(
        default_factory=lambda: resolve_path(
            TRAINING_CONFIG["evaluation"]["confusion_matrix_path"]
        )
    )


# ==========================================
# BATCH PREDICTION CONFIGURATION
# ==========================================

@dataclass
class BatchPredictionConfig:

    root_dir: Path = field(
        default_factory=lambda: resolve_path(
            TRAINING_CONFIG["prediction"]["root_dir"]
        )
    )

    predictions_file_path: Path = field(
        default_factory=lambda: resolve_path(
            TRAINING_CONFIG["prediction"]["predictions_file_path"]
        )
    )

    low_confidence_file_path: Path = field(
        default_factory=lambda: resolve_path(
            TRAINING_CONFIG["prediction"]["low_confidence_file_path"]
        )
    )

    prediction_summary_path: Path = field(
        default_factory=lambda: resolve_path(
            TRAINING_CONFIG["prediction"]["prediction_summary_path"]
        )
    )

    batch_size: int = field(
        default_factory=lambda: TRAINING_CONFIG[
            "prediction"
        ]["batch_size"]
    )

    high_confidence_threshold: float = field(
        default_factory=lambda: TRAINING_CONFIG[
            "prediction"
        ]["high_confidence_threshold"]
    )

    medium_confidence_threshold: float = field(
        default_factory=lambda: TRAINING_CONFIG[
            "prediction"
        ]["medium_confidence_threshold"]
    )

    padding_type: str = field(
        default_factory=lambda: DATA_CONFIG["data_transformation"]["padding_type"]
    )

    truncating_type: str = field(
        default_factory=lambda: DATA_CONFIG["data_transformation"]["truncating_type"]
    )
