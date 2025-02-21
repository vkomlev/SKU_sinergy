# app/api/tables/urls.py

"""
Модуль маршрутов API для работы с таблицами.

Этот модуль содержит маршруты для получения данных, метаданных, поиска, создания, обновления и удаления записей в таблицах.

Функции:
- `setup_table_api_routes(app: Flask) -> None`: Регистрирует API-маршруты в приложении Flask.

Переменные:
- `tables_api`: Blueprint для группировки маршрутов API.
"""

from flask import Blueprint, Flask

from app.api.tables.views import (
    get_data_view,
    get_metadata_view,
    search,
    create_record,
    update_record,
    delete_record,
    get_record
)

tables_api = Blueprint('tables_api', __name__)

# Регистрация маршрутов через Blueprint
def setup_table_api_routes(app: Flask) -> None:
    """
    Регистрирует API-маршруты для работы с таблицами.

    Args:
        app (Flask): Экземпляр Flask-приложения.

    Returns:
        None
    """
    """Получение данных из таблицы."""
    tables_api.add_url_rule('/api/tables/<table_name>/data', 'data', get_data_view)
    """Получение метаданных таблицы."""
    tables_api.add_url_rule('/api/tables/<table_name>/metadata', 'metadata', get_metadata_view)
    '''Поиск записей в таблице.'''
    tables_api.add_url_rule('/api/tables/<table_name>/search', 'search', search)
    '''Создание записи в таблице.'''
    tables_api.add_url_rule('/api/tables/<table_name>/records', 'create_record', create_record, methods=['POST'])
    '''Обновление записи в таблице.'''
    tables_api.add_url_rule('/api/tables/<table_name>/records/<int:record_id>', 'update_record', update_record, methods=['PUT'])
    '''Удаление записи из таблицы.'''
    tables_api.add_url_rule('/api/tables/<table_name>/records/<int:record_id>', 'delete_record', delete_record, methods=['DELETE'])
    '''Получение записи из таблицы.'''
    tables_api.add_url_rule('/api/tables/<table_name>/records/<int:record_id>', 'get_record', get_record, methods=['GET'])
    
    app.register_blueprint(tables_api)