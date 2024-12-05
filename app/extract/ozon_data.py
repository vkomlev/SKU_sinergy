import requests
import json
from datetime import datetime
import logging

import logging_config

logger = logging.getLogger(__name__)

def get_postings(client_id, api_key, from_, to, status="awaiting_deliver", limit=1000, offset=0):
    """
    Функция отправляет запрос к Ozon API для получения списка отправлений.
    
    Args:
        client_id (str): Идентификатор клиента.
        api_key (str): API ключ.
        from_ (str): Дата начала периода в формате ISO (например, "2024-10-01T00:00:00Z").
        to (str): Дата окончания периода в формате ISO (например, "2024-11-30T00:00:00Z").
        status (str): Статус заказов (по умолчанию "awaiting_packaging").
        limit (int): Максимальное количество записей (по умолчанию 1000).
        offset (int): Смещение для пагинации (по умолчанию 0).
        
    Returns:
        dict: Ответ API в формате JSON.
    """
    url = "https://api-seller.ozon.ru/v3/posting/fbs/list"
    headers = {
        "Client-Id": client_id,
        "Api-Key": api_key,
        "Content-Type": "application/json"
    }
    body = {
        "dir": "ASC",
        "filter": {
            "since": from_,
            "to": to,
            "status": status
        },
        "limit": limit,
        "offset": offset,
        "with": {
            "analytics_data": True,
            "barcodes": True,
            "financial_data": True,
            "translit": False
        }
    }
    
    # Отправка POST-запроса
    response = requests.post(url, headers=headers, json=body)
    
    # Проверка успешности запроса
    if response.status_code == 200:
        return response.json().get('result',{}).get('postings', [])  # Возвращаем данные в формате JSON
    else:
        response.raise_for_status()  # Выбрасываем ошибку для неуспешного запроса

def get_posting_detail(client_id: str, api_key: str, posting_number: str):
    """
    Функция отправляет запрос к Ozon API для получения детализации по отправлению.
    
    Args:
        client_id (str): Идентификатор клиента.
        api_key (str): API ключ.
        posting_number (str): Номер отправления.
        
    Returns:
        dict: Ответ API в формате JSON.
    """
    url = "https://api-seller.ozon.ru/v3/posting/fbs/get"
    headers = {
        "Client-Id": client_id,
        "Api-Key": api_key,
        "Content-Type": "application/json"
    }
    body = {
            "posting_number": posting_number,
            "with": {
                "barcodes": False,
                "financial_data": False,
                "product_exemplars": False,
                "translit": False,

            }        
    }
    
    # Отправка POST-запроса
    response = requests.post(url, headers=headers, json=body)
    
    # Проверка успешности запроса
    if response.status_code == 200:
        return response.json()  # Возвращаем данные в dict
    else:
        response.raise_for_status()  # Выбрасываем ошибку для неуспешного запроса