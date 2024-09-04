# app/services/base_service.py

class BaseService:
    def __init__(self, controller):
        self.controller = controller

    def get_with_pagination(self, page, size):
        """Получить данные с пагинацией"""
        offset = (page - 1) * size
        limit = size
        return self.controller.get_page(offset, limit)

    def get_with_sorting(self, **kwargs):
        """Получить данные с сортировкой"""
        return self.controller.sort(**kwargs)
    
    def search_orders(self, **filters):
        """Получить данные по фильтрам"""
        return self.controller.filter_orders(**filters)
