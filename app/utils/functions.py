# app/utils/functions.py
import datetime
import re
import logging
import json

import logging_config
from app.utils.road_distance import RoadDistance
from settings import CLIENTS


logger = logging.getLogger(__name__)

def apply_transformation(value, transformation, func_obj=None, **kwargs):
    """
    Преобразует входное значение с использованием указанного преобразования.
    
    :param value: Исходное значение, которое нужно преобразовать.
    :param transformation: Название преобразования или метода.
    :param func_class: Экземпляр класса, методы которого могут быть вызваны.
    :param kwargs: Дополнительные аргументы для преобразования.
    :return: Преобразованное значение.
    """
    if transformation == 'db_get_key_from_fields':
        service = kwargs.get('service')
        if service:
            return service.get_key_from_fields(value=value, **kwargs)
    elif transformation == 'parse_date_string':
        return parse_date_string(value)
    elif func_obj and hasattr(func_obj, transformation):
        # Проверяем, есть ли указанный метод в классе func_class
        method = getattr(func_obj, transformation)
        if callable(method):
            logger.debug(f"Calling method {transformation} of {func_obj.__class__.__name__} with value: {value} and kwargs: {kwargs}")
            return method(value=value, **kwargs)
    # Можно добавить дополнительные преобразования
    return value


def parse_date_string(value):
    """Parse date range strings and other formats to return the latest date."""
    
    logger.debug(f'Function call parse_date_string({value})')
    # Словарь для преобразования названий месяцев
    months = {
        'января': 1,
        'февраля': 2,
        'марта': 3,
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7,
        'августа': 8,
        'сентября': 9,
        'октября': 10,
        'ноября': 11,
        'декабря': 12
    }
    
    # Список регулярных выражений для поиска дат
    patterns = [
        r'(\d{1,2})[,\s\u202f]*—[,\s\u202f]*(\d{1,2})\s([\wа-яА-ЯёЁ]+)',   # Диапазоны дат, например "12 — 13 августа"
        r'(\d{1,2})-(\d{1,2})\s([\wа-яА-ЯёЁ]+)',                         # Диапазоны, например "12-13 августа"
        r'(\d{1,2})\s([\wа-яА-ЯёЁ]+)',                                   # Одиночные даты, например "7 августа"
        r'(\d{1,2})[,\s\u202f]+(\d{1,2})\s([\wа-яА-ЯёЁ]+)',               # Несколько дат, например "7, 8 сентября"
        r'(\d{1,2})([\wа-яА-ЯёЁ]+)',                                     # Слипшиеся даты, например "7августа"
    ]

    # Функция для поиска всех дат в строке
    def find_dates(text):
        dates = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            logger.debug(f'Fuction find_dates. Matches: {matches}')
            for match in matches:
                if len(match) == 2:  # Одиночная дата (слипшаяся)
                    day, month = match
                else:  # Диапазоны и другие сложные варианты
                    day = match[-2]
                    month = match[-1]
                if month in months:
                    dates.append((int(day), months[month]))
            logger.debug(f'Fuction find_dates. Found dates: {dates}')
        return dates
    
    if isinstance(value, str):
        try:
            # Поиск дат в строке
            found_dates = find_dates(value)
            if not found_dates:
                logger.debug(f'Fuction parse_date_string. Not found dates')
                return None
            
            # Преобразуем найденные даты в объекты datetime.date с текущим годом
            current_year = datetime.datetime.now().year
            date_objects = [datetime.date(current_year, month, day) for day, month in found_dates]
            
            # Возвращаем самую позднюю дату
            return max(date_objects)
        
        except ValueError:
            pass
    
    elif isinstance(value, datetime.date):
        logger.debug(f'Fuction parse_date_string. Found dates: {value}')
        return value
    
    # Если не удалось найти даты, возвращаем None
    return None

class OzonTransfomationFunctions:
    def __init__(self, id_client = None):
        self.id_client = id_client
        self.distance = 0
        self.climb = False

    def _get_service(self, table_name):
        from app.utils.helpers import get_session
        from app.services.base_service import BaseService
        from app.repositories.base_repository import BaseRepository
        from app.controllers.base_controller import BaseController
        model = BaseRepository.get_model_by_table_name(table_name)
        session = get_session()
        self.service = BaseService(BaseController(BaseRepository(model, session)))

    def get_ozon_id(self, value=None):
        
        self._get_service('main.marketpalces')
        result = self.service.get_key_from_fields(field_name = 'mp_name', value = 'Ozon', key_name = 'id_marketplace')
        logger.info(f'Fuction get_ozon_id. Result: {result}')
        return result
    
    def get_ozon_client_id(self, value=None):
        
        logger.info(f'Fuction get_ozon_client_id. Result: {self.id_client}')
        return self.id_client

    def get_ozon_product_id(self,value=None):
        if value:
            self._get_service('main.products')
            result = self.service.get_key_from_fields(field_name = 'sku', value = value, key_name = 'id_product')
            logger.info(f'Fuction get_ozon_product_id. Result: {result}')
            return result
        logger.warning(f'Fuction get_ozon_product_id. Нет значения SKU для поиска товара.')
        return None
    
    def get_ozon_client_phone(self,value , **kwargs):
        result = value
        if kwargs.get('posting_number'):
            from app.extract.ozon_data import get_posting_detail
            id = CLIENTS.get(self.id_client, {} ).get('id_ozon','')
            api = CLIENTS.get(self.id_client, {}).get('api_ozon','')
            data = get_posting_detail(id, api, kwargs.get('posting_number'))
            return result+ '\n' + data.get('result',{}).get('customer',{}).get('phone', '')

    def get_ozon_climb(self, value):
        if value == 'none' :
            self.climb = False
            return 'Не включен'
        elif value:
            self.climb = True
            return 'Включен'
        else:
            self.climb= False
            return 'Не указано'

    def get_ozon_status(self, value=None):
        self._get_service('main.delivery_status')
        result = self.service.get_key_from_fields(field_name = 'ds_name', value = 'Новая', key_name = 'id_ds')
        logger.info(f'Fuction get_ozon_status. Result: {result}')
        return result
    
    def get_ozon_distance(self, value, **kwargs):
        if kwargs.get('latitude') and kwargs.get('longitude'):
            params = {'lat': kwargs.get('latitude'), 'lng': kwargs.get('longitude')}
            params = json.dumps(params)
            rd = RoadDistance()
            result = float(rd.get_mkad_distance(params).get('distance',0))/1000
            self.distance = result
            logger.info(f'Fuction get_ozon_distance. Result: {result}')
            return result
        elif value:
            rd = RoadDistance()
            result = float(rd.get_mkad_distance(value).get('distance',0))/1000
            self.distance = result
            logger.info(f'Fuction get_ozon_distance. Result: {result}')
            return result
        logger.warning(f'Fuction get_ozon_distance. Нет значения Address для расчета расстояния.')
        return None
    
    def get_ozon_delivery_name(self, value=None):
        self._get_service('main.delivery_company')
        result = self.service.get_key_from_fields(field_name = 'dc_name', value = 'Акоп', key_name = 'id_dc')
        logger.info(f'Fuction get_ozon_delivery_name. Result: {result}')
        return result

    def get_ozon_cost(self, value=None):
        cost = 1200 + self.distance*35
        if self.climb:
            cost+= 500
        logger.info(f'Fuction get_ozon_cost. Result: {cost}')
        return cost
    
    def parse_date_string(self, value):
        return parse_date_string(value)


