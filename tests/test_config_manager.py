
from civicsense.entity.config_manager import ConfigurationManager


# Initialize configuration manager
config_manager = ConfigurationManager()


# Load configurations
data_config = config_manager.get_data_config()
model_config = config_manager.get_model_config()
training_config = config_manager.get_training_config()


# Verify important configuration values
assert data_config["data_transformation"]["max_sequence_length"] == 156

assert data_config["data_transformation"]["embedding_dimension"] == 100

assert model_config["model"]["lstm_units"] == 64

assert model_config["model"]["dropout_rate"] == 0.3

assert training_config["training"]["epochs"] == 15

assert training_config["training"]["batch_size"] == 64

assert training_config["prediction"]["high_confidence_threshold"] == 0.80


print("\nCONFIGURATION MANAGER TEST")
print("--------------------------")

print("Maximum sequence length:", data_config["data_transformation"]["max_sequence_length"])
print("Embedding dimension:", data_config["data_transformation"]["embedding_dimension"])
print("LSTM units:", model_config["model"]["lstm_units"])
print("Dropout rate:", model_config["model"]["dropout_rate"])
print("Training epochs:", training_config["training"]["epochs"])
print("Batch size:", training_config["training"]["batch_size"])

print("\nConfiguration Manager Test Successful!")
