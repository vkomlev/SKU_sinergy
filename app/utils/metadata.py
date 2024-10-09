#app/utils/metadata.py

import json
import os
from settings import METADATA_DIR
from app.utils.helpers import get_session


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
    
    def get_unique_columns(self, table_name):
        """Возвращает список уникальных столбцов для таблицы"""
        metadata = self.get_metadata(table_name.replace('.', '_', 1))
        columns = metadata["columns"]
        unique_columns = [col for col in columns if col.get("mappings",{"unique_key": False}).get("unique_key", False)==True]
        return unique_columns
    
    @staticmethod
    def save_to_file(table_name):
        """Сохраняет метаданные в JSON-файл с расширенными параметрами."""
        from app.repositories.base_repository import BaseRepository
        model = BaseRepository.get_model_by_table_name(table_name.replace('_', '.', 1))
        session = get_session()
        br = BaseRepository(model, session)
        metadata = br.get_table_metadata()

        # Добавление логики заполнения дополнительных параметров
        for column in metadata['columns']:
            # Установка параметра "visible" на false для первичных ключей
            column['visible'] = not column['primary_key']

            # Установка "transformation" на "skip" для первичных ключей
            column['mappings'] = column.get('mappings', {})
            if column['primary_key']:
                column['mappings']['transformation'] = 'skip'
            else:
                column['mappings']['transformation'] = 'direct'

            # Автоматическое определение input_type в зависимости от типа данных
            if column['type'].lower() in ['integer', 'smallint', 'bigint']:
                column['input_type'] = 'number'
            elif column['type'].lower() in ['float', 'double precision', 'numeric', 'money']:
                column['input_type'] = 'number'
            elif column['type'].lower() in ['string', 'text', 'varchar', 'char']:
                column['input_type'] = 'text'
            elif column['type'].lower() in ['boolean']:
                column['input_type'] = 'checkbox'
            elif column['type'].lower() in ['datetime', 'timestamp']:
                column['input_type'] = 'datetime'
            elif column['type'].lower() in ['date']:
                column['input_type'] = 'date'
            else:
                column['input_type'] = 'text'

        # Сохранение в файл
        file_path = os.path.join(MetadataManager.get_metadata_dir(), f"{table_name}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)
    
    @staticmethod
    def get_metadata_dir():
        return METADATA_DIR


