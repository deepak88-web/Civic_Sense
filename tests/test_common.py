
from pathlib import Path

from civicsense.utils.common import (
    create_directories,
    write_yaml_file,
    read_yaml_file,
    save_object,
    load_object
)


# Test directory creation
create_directories(["artifacts/test"])

# Test YAML operations
yaml_path = Path("artifacts/test/config.yaml")

data = {
    "model": "LSTM",
    "embedding_dimension": 100,
    "max_length": 156
}

write_yaml_file(yaml_path, data)
loaded_data = read_yaml_file(yaml_path)

print("YAML Test:", loaded_data)


# Test object serialization
object_path = Path("artifacts/test/test_object.pkl")

save_object(object_path, data)
loaded_object = load_object(object_path)

print("Object Test:", loaded_object)


print("All tests completed successfully!")
