
from civicsense.components.data_ingestion import DataIngestion
from civicsense.components.data_validation import DataValidation

from civicsense.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig
)


# Step 1: Run data ingestion
ingestion = DataIngestion(
    data_ingestion_config=DataIngestionConfig()
)

ingestion_artifact = ingestion.initiate_data_ingestion()


# Step 2: Run data validation
validation = DataValidation(
    data_validation_config=DataValidationConfig(),
    data_ingestion_artifact=ingestion_artifact
)

validation_artifact = validation.initiate_data_validation()


# Step 3: Check results
print("\nData Validation Test Successful!")
print("Validation Status:", validation_artifact.validation_status)
print("Message:", validation_artifact.validation_message)

assert validation_artifact.validation_status is True

print("\nBoth datasets passed validation.")
