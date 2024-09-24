# app/controllers/base_controller.py

from app.utils.metadata import MetadataManager
from app.repositories.base_repository import BaseRepository
from sqlalchemy.inspection import inspect
from settings import UPLOAD_DIR
from werkzeug.utils import secure_filename
import os
import uuid
import pandas as pd
from app.utils.functions import apply_transformation

class BaseController:
    def __init__(self, repository):
        self.repo = repository
        self.metadata_manager = MetadataManager()
        self.allowed_extensions_for_load_table = {'csv', 'xlsx'}
        self.allowed_extensions_for_mediafile = {'jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi'}

    def get_combined_metadata(self):
        """Получить комбинированные метаданные"""
        db_metadata = self.repo.get_table_metadata()
        table_name = db_metadata['table_name']

        
        json_metadata = self.metadata_manager.get_metadata(table_name) # Получение метаданных из JSON-файла
        json_columns_map = {column['name']: column for column in json_metadata.get('columns', [])}

        combined_columns = []
        for db_column in db_metadata['columns']:
            json_column = json_columns_map.get(db_column['name'], {})
            combined_column = db_column | json_column  # Объединение метаданных из БД и JSON

            combined_columns.append(combined_column)

        combined_metadata = {
            "table_name": table_name,
            "columns": combined_columns
        }

        return combined_metadata

    def get_page(self, offset, limit):
        """Получить страницу записей"""
        return self.repo.get_page(offset, limit)
    
    def get_count(self):
        """Получить количество записей"""
        return self.repo.get_count()


    def sort (self, **kwargs):
        """Сортировка"""
        return self.repo.sort_by_fields(**kwargs)

    def get_by_id(self, entity_id):
        """Получить запись по ID"""
        return self.repo.get_by_id(entity_id)
    
    def filter_records(self, **filters):
        """Получить отфильтрованные данные"""
        return self.repo.filter_by_fields(**filters)

    def search(self, query):
        """Поиск по строке"""
        return self.repo.search(query)

    def create_record(self, data, table):
        """Создать новую запись"""
        data = self.from_dict (table, data)
        return self.repo.add(data)

    def update_record(self, record_id, data):
        """Обновить существующую запись"""
        record = self.repo.get_by_id(record_id)
        if record:
            return self.repo.update(record, data)
        return None

    def delete_record(self, record_id):
        """Удалить запись"""
        record = self.repo.get_by_id(record_id)
        if record:
            self.repo.delete(record)
            return True
        return False
    
    @staticmethod
    def to_dict(self, obj):
        """Преобразует объект модели в словарь"""
        return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}
    
    def from_dict(self, table_name: str, data: dict):
        """
        Универсальный метод для создания экземпляра модели на основе названия таблицы и данных.
        """
        # Получаем класс модели по имени таблицы
        model_class = BaseRepository.get_model_by_table_name(table_name)

        # Создаем пустой экземпляр модели
        model_instance = model_class()

        # Получаем список всех колонок модели
        mapper = inspect(model_class)

        # Заполняем поля модели значениями из словаря data
        for column in mapper.attrs:
            column_name = column.key
            if column_name in data:
                setattr(model_instance, column_name, data[column_name])

        return model_instance
    
    def __allowed_file(self, filename: str, filetype: str):
        """Проверка разрешенного файла"""
        if filetype == 'data':
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions_for_load_table
        elif filetype == 'media':
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions_for_mediafile


    def upload_file(self, file, filetype = 'media'):
        """Загрузить файл на сервер"""
        if file and self.__allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_id = str(uuid.uuid4())  # Генерация уникального идентификатора для файла
            file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{filename}")
            file.save(file_path)
            return file_id
        return None
    
    def transform_file(self, file):
        '''Преобразование загруженного файла данных по мапингу'''
        s = file.read()
        # Определяем формат файла
        try:
            if file.filename.endswith('.csv'):
                data = pd.read_csv(file, delimiter=';')
            elif file.filename.endswith(('.xls', '.xlsx')):
                data = pd.read_excel(file)
            else:
                return {"status": "fail", "message": "Unsupported file format"}, 400
        except Exception as e:
            return {"status": "fail", "message": f"Error reading file: {e}"}, 400
        
        data = data.to_dict(orient='records')
        return self.apply_mapping(data)

    def apply_mapping(self, data):
        """Применение маппинга к данным с преобразованием типов"""

        metadata = self.get_combined_metadata()
        # Применяем маппинг и преобразования
        transformed_data = []
        
        # Функция для приведения типов
        def convert_to_type(value, column_type):
            if value is None:
                return None
            try:
                if column_type == 'integer':
                    return int(value)
                elif column_type == 'float':
                    return float(value)
                elif column_type == 'string':
                    return str(value)
                elif column_type == 'boolean':
                    return bool(value)
                # Добавляем другие типы данных при необходимости
                else:
                    return value
            except (ValueError, TypeError):
                # Обработка ошибок приведения типов, например, возвращаем значение как есть или None
                return None

        for row in data:
            transformed_row = {}
            for col_meta in metadata['columns']:
                source_column = col_meta['mappings'].get('import_name', None)
                transformation = col_meta['mappings'].get('transformation', 'direct')
                column_type = col_meta.get('type', 'string')  # Получаем тип данных из метаданных

                if transformation == 'skip':
                    continue
                elif transformation == 'direct':
                    # Прямое сопоставление с преобразованием типа
                    transformed_row[col_meta['name']] = convert_to_type(row[source_column], column_type)
                else:
                    # Применение функции преобразования с последующим приведением типа
                    transformed_value = apply_transformation(row[source_column], transformation)
                    transformed_row[col_meta['name']] = convert_to_type(transformed_value, column_type)
            
            transformed_data.append(transformed_row)

        # Передаем данные в репозиторий для сохранения
        return transformed_data

    
    def load_transformed_data(self, file):
        data = self.transform_file(file)
        if isinstance(data, dict):
            return data
        else:
            try:
                self.repo.save_import_data_to_table(data)
            except Exception as e:
                return {"status": "fail", "message": f"Error saving data: {e}"}, 400
            return {"status": "success", "message": "Data saved successfully"}, 200



