
from civicsense.components.data_ingestion import DataIngestion
from civicsense.entity.config_entity import DataIngestionConfig


# Initialize configuration
config = DataIngestionConfig()

# Initialize data ingestion component
data_ingestion = DataIngestion(
    data_ingestion_config=config
)

# Execute data ingestion
artifact = data_ingestion.initiate_data_ingestion()

# Display results
print("\nData Ingestion Test Successful!")

print(
    "\nSupervised Dataset:",
    artifact.supervised_data_file_path
)

print(
    "Prediction Dataset:",
    artifact.prediction_data_file_path
)

# Verify output files
assert artifact.supervised_data_file_path.exists()
assert artifact.prediction_data_file_path.exists()

print("\nBoth output files exist.")
