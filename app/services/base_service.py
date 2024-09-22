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
    
    def get_count(self):
        """Получить количество записей"""
        return self.controller.get_count()


    def sort(self, **kwargs):
        """Получить данные с сортировкой"""
        return self.controller.sort(**kwargs)
    
    def filter(self, **filters):
        """Получить данные по фильтрам"""
        return self.controller.filter_records(**filters)

    def get_table_metadata(self):
        """Получить метаданные таблицы"""
        return self.controller.get_combined_metadata()
    
    def search(self, query):
        """Поиск по строке"""
        return self.controller.search(query)
    
    def create_data(self, data, table):
        """Создать данные"""
        return self.controller.create_record(data, table)

    def update_data(self, record_id, data):
        """Обновить данные"""
        return self.controller.update_record(record_id, data)

    def delete_data(self, record_id):
        """Удалить данные"""
        return self.controller.delete_record(record_id)
    
    def get_record(self, record_id):
        """Получить данные по id"""
        return self.controller.get_by_id(record_id)

   
