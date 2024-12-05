# app/utils/helpers.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import DATABASE
from datetime import datetime, timedelta
import calendar
import re

from app.services.base_service import BaseService
from app.repositories.base_repository import BaseRepository
from app.controllers.base_controller import BaseController

def get_engine():
    return create_engine(f"{DATABASE['drivername']}://{DATABASE['username']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['database']}")

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

def create_service(table_name, **kwargs):
    session = get_session()
    model = BaseRepository.get_model_by_table_name(table_name.replace('_', '.', 1))
    service = BaseService(BaseController(BaseRepository(model, session)))
    return service

def get_date_range():
    """
    Формирует даты:
    - FROM: первое число предыдущего месяца.
    - TO: последнее число текущего месяца.
    
    Returns:
        tuple: (FROM, TO) в формате ISO8601.
    """
    # Текущая дата
    now = datetime.now()
    
    # Вычисляем первое число предыдущего месяца
    first_day_prev_month = (now.replace(day=1) - timedelta(days=1)).replace(day=1)
    
    # Вычисляем последнее число текущего месяца
    _, last_day_of_month = calendar.monthrange(now.year, now.month)
    last_day_curr_month = now.replace(day=last_day_of_month, hour=23, minute=59, second=59, microsecond=0)
    
    # Преобразуем даты в строковый формат ISO8601
    from_ = first_day_prev_month.strftime("%Y-%m-%dT%H:%M:%SZ")
    to = last_day_curr_month.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    return from_, to

def get_value_by_path(data, path):
    """
    Извлекает значение из словаря/списка на основе пути.
    
    :param data: Входной словарь или список (JSON-объект).
    :param path: Путь к ключу (например, "products[0].offer_id").
    :return: Значение по указанному пути или None, если путь неверный.
    """
    # Разбиваем путь на ключи и индексы
    keys = re.split(r'\.|\[|\]', path)
    keys = [key for key in keys if key]  # Убираем пустые элементы
    
    # Проходим по ключам/индексам
    current = data
    try:
        for key in keys:
            # Если ключ - это индекс списка
            if key.isdigit():
                current = current[int(key)]
            else:
                current = current[key]
    except (KeyError, IndexError, TypeError):
        return None  # Если путь некорректный, возвращаем None
    return current