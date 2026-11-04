
import os
import yaml
import json
import dill

from pathlib import Path
from typing import Any

from civicsense.logger import get_logger
from civicsense.exception import CivicSenseException

import sys


logger = get_logger(__name__)


def create_directories(path_to_directories: list):

    try:
        for path in path_to_directories:
            os.makedirs(path, exist_ok=True)
            logger.info(f"Directory created or already exists: {path}")

    except Exception as e:
        raise CivicSenseException(e, sys)


def read_yaml_file(path: Path) -> dict:

    try:
        with open(path, "rb") as yaml_file:
            content = yaml.safe_load(yaml_file)

        return content if content is not None else {}

    except Exception as e:
        raise CivicSenseException(e, sys)


def write_yaml_file(path: Path, content: dict) -> None:

    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as yaml_file:
            yaml.dump(content, yaml_file, sort_keys=False)

        logger.info(f"YAML file saved: {path}")

    except Exception as e:
        raise CivicSenseException(e, sys)


def read_json_file(path: Path) -> Any:

    try:
        with open(path, "r", encoding="utf-8") as json_file:
            content = json.load(json_file)

        return content

    except Exception as e:
        raise CivicSenseException(e, sys)


def write_json_file(path: Path, content: Any) -> None:

    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as json_file:
            json.dump(content, json_file, indent=4)

        logger.info(f"JSON file saved: {path}")

    except Exception as e:
        raise CivicSenseException(e, sys)


def save_object(file_path: Path, obj: Any) -> None:

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

        logger.info(f"Object saved successfully: {file_path}")

    except Exception as e:
        raise CivicSenseException(e, sys)


def load_object(file_path: Path) -> Any:

    try:
        with open(file_path, "rb") as file_obj:
            obj = dill.load(file_obj)

        logger.info(f"Object loaded successfully: {file_path}")

        return obj

    except Exception as e:
        raise CivicSenseException(e, sys)
