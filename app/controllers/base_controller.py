# app/controllers/base_controller.py

from app.utils.metadata import MetadataManager
from app.repositories.base_repository import BaseRepository
from sqlalchemy.inspection import inspect

class BaseController:
    def __init__(self, repository):
        self.repo = repository
        self.metadata_manager = MetadataManager()

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
    
    def filter_orders(self, **filters):
        """Получить отфильтрованные заказы"""
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