#app/utils/metadata.py

import json
import os
from settings import METADATA_DIR


class MetadataManager:
    def __init__(self):
        self.metadata_dir = METADATA_DIR

    def get_metadata(self, table_name):
        """Загружает метаданные из JSON-файла"""
        try:
            file_path = os.path.join(self.metadata_dir, f"{table_name}.json")
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise ValueError(f"Metadata for table '{table_name}' not found.")