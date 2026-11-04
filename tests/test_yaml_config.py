
from pathlib import Path

from civicsense.utils.common import read_yaml_file


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

CONFIG_DIR = PROJECT_ROOT / "config"


# Step 1: Load data.yaml
data_config = read_yaml_file(
    CONFIG_DIR / "data.yaml"
)


# Step 2: Load model.yaml
model_config = read_yaml_file(
    CONFIG_DIR / "model.yaml"
)


# Step 3: Load training.yaml
training_config = read_yaml_file(
    CONFIG_DIR / "training.yaml"
)


# Step 4: Verify configuration sections
assert "data_ingestion" in data_config
assert "data_validation" in data_config
assert "data_transformation" in data_config

assert "model" in model_config

assert "training" in training_config
assert "evaluation" in training_config
assert "prediction" in training_config


# Step 5: Display loaded configurations
print("\nYAML CONFIGURATION TEST")
print("-----------------------")

print("Data configuration sections:", list(data_config.keys()))
print("Model configuration sections:", list(model_config.keys()))
print("Training configuration sections:", list(training_config.keys()))

print("\nYAML Configuration Test Successful!")
