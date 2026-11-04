
from pathlib import Path

from civicsense.utils.common import read_yaml_file


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[3]

CONFIG_DIR = PROJECT_ROOT / "config"


class ConfigurationManager:

    def __init__(self):

        # Load all YAML configuration files
        self.data_config = read_yaml_file(
            CONFIG_DIR / "data.yaml"
        )

        self.model_config = read_yaml_file(
            CONFIG_DIR / "model.yaml"
        )

        self.training_config = read_yaml_file(
            CONFIG_DIR / "training.yaml"
        )

    def get_data_config(self):

        return self.data_config

    def get_model_config(self):

        return self.model_config

    def get_training_config(self):

        return self.training_config
