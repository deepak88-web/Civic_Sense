
import numpy as np

from civicsense.components.data_ingestion import DataIngestion
from civicsense.components.data_validation import DataValidation
from civicsense.components.data_transformation import DataTransformation

from civicsense.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig
)


# Step 1: Data Ingestion
ingestion = DataIngestion(
    data_ingestion_config=DataIngestionConfig()
)

ingestion_artifact = ingestion.initiate_data_ingestion()


# Step 2: Data Validation
validation = DataValidation(
    data_validation_config=DataValidationConfig(),
    data_ingestion_artifact=ingestion_artifact
)

validation_artifact = validation.initiate_data_validation()


# Step 3: Data Transformation
transformation = DataTransformation(
    data_transformation_config=DataTransformationConfig(),
    data_validation_artifact=validation_artifact
)

transformation_artifact = transformation.initiate_data_transformation()


# Step 4: Verify transformed datasets
transformed_data = np.load(
    transformation_artifact.transformed_data_file_path
)

print("\nTransformed Dataset Shapes:")
print("X_train:", transformed_data["X_train"].shape)
print("X_val:", transformed_data["X_val"].shape)
print("X_test:", transformed_data["X_test"].shape)

print("\nEncoded Label Shapes:")
print("y_train:", transformed_data["y_train"].shape)
print("y_val:", transformed_data["y_val"].shape)
print("y_test:", transformed_data["y_test"].shape)


# Step 5: Verify embedding matrix
embedding_matrix = np.load(
    transformation_artifact.embedding_matrix_file_path
)

print("\nEmbedding Matrix Shape:", embedding_matrix.shape)


# Step 6: Verify all artifacts exist
assert transformation_artifact.transformed_data_file_path.exists()
assert transformation_artifact.tokenizer_file_path.exists()
assert transformation_artifact.label_encoder_file_path.exists()
assert transformation_artifact.max_sequence_length_file_path.exists()
assert transformation_artifact.embedding_matrix_file_path.exists()
assert transformation_artifact.word2vec_model_file_path.exists()

assert transformed_data["X_train"].shape[1] == 156
assert transformed_data["X_val"].shape[1] == 156
assert transformed_data["X_test"].shape[1] == 156

assert embedding_matrix.shape[1] == 100

print("\nData Transformation Test Successful!")
print("All transformation artifacts have been generated.")
