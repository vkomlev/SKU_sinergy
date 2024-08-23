# app/services/base_service.py

class BaseService:
    def __init__(self, controller):
        self.controller = controller

    def get_with_pagination(self, page, per_page):
        """Получить данные с пагинацией"""
        offset = (page - 1) * per_page
        return self.controller.get_page(offset, per_page)
