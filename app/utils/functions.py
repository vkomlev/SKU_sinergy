# app/utils/functions.py

from app.services.base_service import BaseService
import datetime
import re

def apply_transformation(value, transformation, **kwargs):
    if transformation == 'db_get_key_from_fields':
        service = kwargs.get('service')
        if service:
            return service.get_key_from_fields(value=value, **kwargs)
    elif transformation == 'parse_date_string':
        return parse_date_string(value)
    # Можно добавить дополнительные преобразования
    return value

def parse_date_string(value):
    """Parse date range strings and other formats to return the latest date."""
    
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
            for match in matches:
                if len(match) == 2:  # Одиночная дата (слипшаяся)
                    day, month = match
                else:  # Диапазоны и другие сложные варианты
                    day = match[-2]
                    month = match[-1]
                if month in months:
                    dates.append((int(day), months[month]))
        return dates
    
    if isinstance(value, str):
        try:
            # Поиск дат в строке
            found_dates = find_dates(value)
            if not found_dates:
                return None
            
            # Преобразуем найденные даты в объекты datetime.date с текущим годом
            current_year = datetime.datetime.now().year
            date_objects = [datetime.date(current_year, month, day) for day, month in found_dates]
            
            # Возвращаем самую позднюю дату
            return max(date_objects)
        
        except ValueError:
            pass
    
    elif isinstance(value, datetime.date):
        return value
    
    # Если не удалось найти даты, возвращаем None
    return None
