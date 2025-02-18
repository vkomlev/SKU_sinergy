# app/model_registry.py

"""
Модуль регистрации моделей базы данных.

Этот модуль предоставляет функции для регистрации моделей SQLAlchemy и получения модели по названию таблицы.
Используется для централизованного управления моделями в системе.

Функции:
- `register_model(model)`: Регистрирует модель в реестре моделей.
- `get_model_by_table_name(table_name)`: Возвращает модель по имени таблицы.

Переменные:
- `model_registry`: Словарь, содержащий зарегистрированные модели.
"""
from sqlalchemy import Table

model_registry = {}

def register_model(model):
    """
    Регистрирует модель SQLAlchemy в реестре `model_registry`.

    Если модель является экземпляром `Table`, используется её имя `model.name` и схема `model.schema`.
    Если это класс модели, берётся `__tablename__` и `__table_args__`.

    Args:
        model (Union[Table, DeclarativeMeta]): Модель SQLAlchemy.

    Returns:
        None
    """
    if isinstance(model, Table):
        table_name = model.name
        schema = model.schema
    else:
        table_name = model.__tablename__
        args = model.__table_args__ if hasattr(model, '__table_args__') else None
        schema = None
        if args:
            schema = args[-1].get('schema') if isinstance(args, tuple) else args.get('schema')

    if schema:
        table_name = f"{schema}.{table_name}"  # Учитываем схему

    model_registry[table_name.lower()] = model


def get_model_by_table_name(table_name):
    """
    Возвращает зарегистрированную модель по названию таблицы.

    Args:
        table_name (str): Название таблицы (регистр не учитывается).

    Returns:
        DeclarativeMeta: Найденная модель.

    Raises:
        ValueError: Если модель не найдена.
    """
    from app.model_import import DBSDelivery, OrdersOzon
    from app.model_main import Products

    model = model_registry.get(table_name.lower())
    if model is None:
        raise ValueError(f"Модель для таблицы '{table_name}' не найдена.")
    return model
