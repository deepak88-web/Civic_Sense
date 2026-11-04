
import json

from civicsense.components.model_evaluation import ModelEvaluation

from civicsense.entity.config_entity import (
    DataTransformationConfig,
    ModelTrainerConfig,
    ModelEvaluationConfig
)

from civicsense.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact
)


# Step 1: Create transformation artifact
transformation_config = DataTransformationConfig()

transformation_artifact = DataTransformationArtifact(
    transformed_data_file_path=transformation_config.transformed_data_path,
    tokenizer_file_path=transformation_config.tokenizer_path,
    label_encoder_file_path=transformation_config.label_encoder_path,
    max_sequence_length_file_path=transformation_config.max_len_path,
    embedding_matrix_file_path=transformation_config.embedding_matrix_path,
    word2vec_model_file_path=transformation_config.word2vec_model_path
)


# Step 2: Create model trainer artifact
trainer_config = ModelTrainerConfig()

trainer_artifact = ModelTrainerArtifact(
    trained_model_file_path=trainer_config.model_path,
    training_history_file_path=trainer_config.training_history_path
)


# Step 3: Initialize model evaluation
evaluation = ModelEvaluation(
    model_evaluation_config=ModelEvaluationConfig(),
    data_transformation_artifact=transformation_artifact,
    model_trainer_artifact=trainer_artifact
)


# Step 4: Evaluate model
evaluation_artifact = evaluation.initiate_model_evaluation()


# Step 5: Display metrics
with open(
    evaluation_artifact.metrics_file_path,
    "r",
    encoding="utf-8"
) as file:
    metrics = json.load(file)

print("\nFINAL TEST EVALUATION RESULTS")
print("--------------------------------")

for metric, score in metrics.items():
    print(f"{metric}: {score:.4f}")


# Step 6: Verify generated files
assert evaluation_artifact.metrics_file_path.exists()
assert evaluation_artifact.classification_report_file_path.exists()
assert evaluation_artifact.confusion_matrix_file_path.exists()

print("\nModel Evaluation Test Successful!")
print("All evaluation files have been generated.")
