import json
from typing import Any, Dict


def load_from_file(file_path: str) -> Dict[str, Any]:
    with open(file_path, "r") as file:
        data = json.load(file)
    return data
