# app/services/base_service.py


class BaseService:
    def __init__(self, controller):
        self.controller = controller

    def get_table_metadata(self):
        """получить метаданные таблицы"""
        return self.controller.get_combined_metadata()

    def get_with_pagination(self, page, size):
        """Получить данные с пагинацией"""
        offset = (page - 1) * size
        limit = size
        return self.controller.get_page(offset, limit)

    def sort(self, **kwargs):
        """Получить данные с сортировкой"""
        return self.controller.sort(**kwargs)
    
    def filter(self, **filters):
        """Получить данные по фильтрам"""
        return self.controller.filter_orders(**filters)

    def get_table_metadata(self):
        """Получить метаданные таблицы"""
        return self.controller.get_combined_metadata()
    
    def search(self, query):
        """Поиск по строке"""
        return self.controller.search(query)