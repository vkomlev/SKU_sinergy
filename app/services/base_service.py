# app/services/base_service.py
import logging

from settings import CLIENTS
from app.utils.functions import OzonTransfomationFunctions
from app.extract.ozon_data import get_postings
import logging_config

logger = logging.getLogger(__name__)
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
    
    def upload_file_to_server(self, file, filetype='media'):
        """Загрузить файл"""
        return self.controller.upload_file(file, filetype)
    
    def load_transormed_data(self, file):
        """Загрузить трансформированные данные в БД"""
        return self.controller.load_transformed_data(file)
    
    def get_key_from_fields(self, **kwargs):
        """Получить ключ по значению полей"""
        return self.controller.get_key_from_fields(**kwargs)
    
    def extract_ozon_dbs(self):
        '''Получить и загрузить данные по доставкам ОЗОН'''
        from app.utils.helpers import get_date_range
        try:
            from_, to = get_date_range()
            for client, value in CLIENTS.items():
                
                data = get_postings(value.get('id_ozon'), value.get('api_ozon'),from_, to)
                if data:
                    ozon = OzonTransfomationFunctions(client)
                    db_data = self.controller.apply_mapping(data, ozon)
                    self.controller.repo.save_import_data_to_table(db_data)
                else:
                    logger.warning(f"No data for id_client = {client}")
        except Exception as e:
            logger.error(e)
            return {"status": "fail", "message": f"Error saving data: {e}"}, 400
        return {"status": "success", "message": "Data saved successfully"}, 200
   

    
    


   
