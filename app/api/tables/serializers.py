# app/api/tables/serializers.py

"""
Модуль сериализации данных для API.

Использует Marshmallow для автоматического создания схем на основе моделей SQLAlchemy.

Функции:
- `get_field_class(column_type: type) -> type[fields.Field]`: Определяет тип поля Marshmallow по типу SQLAlchemy.

Классы:
- `UniversalSerializer`: Универсальный сериализатор, автоматически создающий поля на основе модели SQLAlchemy.

Переменные:
- `SQLALCHEMY_TYPE_MAPPING`: Словарь для сопоставления типов SQLAlchemy и Marshmallow.
"""


from marshmallow import Schema, fields
from sqlalchemy.orm import class_mapper
from sqlalchemy import Table, Integer, String, DateTime, Float, Boolean, Date
import datetime
from typing import Type

from app.utils.functions import parse_date_string

# Словарь для сопоставления типов SQLAlchemy и Marshmallow
SQLALCHEMY_TYPE_MAPPING = {
    Integer: fields.Int,
    String: fields.Str,
    DateTime: fields.DateTime,
    Float: fields.Float,
    Boolean: fields.Bool,
    Date: fields.Date,
}

def get_field_class(column_type: type) -> Type[fields.Field]:
    """
    Возвращает соответствующий класс поля Marshmallow на основе типа SQLAlchemy.

    Args:
        column_type (type): Тип столбца SQLAlchemy.

    Returns:
        Type[fields.Field]: Соответствующий класс поля Marshmallow.
    """

    for sqlalchemy_type, marshmallow_field in SQLALCHEMY_TYPE_MAPPING.items():
        if isinstance(column_type, sqlalchemy_type):
            return marshmallow_field
    return fields.Str  # По умолчанию строковое поле

class UniversalSerializer(Schema):
    """
    Универсальный сериализатор, автоматически создающий поля на основе модели SQLAlchemy.

    Args:
        model (Type[Table] | Type): Модель SQLAlchemy (класс или таблица).

    Attributes:
        dump_fields (dict): Словарь полей для сериализации.
    """


    def __init__(self, model: Type[Table] | Type, *args, **kwargs) -> None:
        """
        Инициализирует сериализатор, динамически создавая поля на основе модели.

        Args:
            model (Type[Table] | Type): Модель SQLAlchemy.
        """

        super().__init__(*args, **kwargs)
        # Получаем столбцы модели
        if isinstance(model, Table):
            columns = model.columns
        else:
            columns = class_mapper(model).columns
        
        for column in columns:
            field_class = get_field_class(column.type)
            self.dump_fields[column.name] = field_class(attribute=column.name)
            
        