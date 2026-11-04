
from civicsense.components.model_trainer import ModelTrainer

from civicsense.entity.config_entity import (
    DataTransformationConfig,
    ModelTrainerConfig
)

from civicsense.entity.artifact_entity import (
    DataTransformationArtifact
)


# Step 1: Load transformation configuration
transformation_config = DataTransformationConfig()


# Step 2: Create transformation artifact
transformation_artifact = DataTransformationArtifact(
    transformed_data_file_path=transformation_config.transformed_data_path,
    tokenizer_file_path=transformation_config.tokenizer_path,
    label_encoder_file_path=transformation_config.label_encoder_path,
    max_sequence_length_file_path=transformation_config.max_len_path,
    embedding_matrix_file_path=transformation_config.embedding_matrix_path,
    word2vec_model_file_path=transformation_config.word2vec_model_path
)


# Step 3: Initialize model trainer
model_trainer = ModelTrainer(
    model_trainer_config=ModelTrainerConfig(),
    data_transformation_artifact=transformation_artifact
)


# Step 4: Train the model
trainer_artifact = model_trainer.initiate_model_training()


# Step 5: Verify generated artifacts
assert trainer_artifact.trained_model_file_path.exists()
assert trainer_artifact.training_history_file_path.exists()

print("\nModel Training Test Successful!")

print(
    "Trained Model:",
    trainer_artifact.trained_model_file_path
)

print(
    "Training History:",
    trainer_artifact.training_history_file_path
)

print("\nBoth training artifacts exist.")
