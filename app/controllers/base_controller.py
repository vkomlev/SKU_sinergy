# app/controllers/base_controller.py

class BaseController:
    def __init__(self, repository):
        self.repo = repository

    def get_combined_metadata(self):
        """Получить комбинированные метаданные"""
        return self.repo.get_table_metadata()

    def get_page(self, offset, limit):
        """Получить страницу записей"""
        return self.repo.get_page(offset, limit)

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

    @classmethod
    def to_dict(self, obj):
        """Преобразует объект модели в словарь"""
        return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}