# app/api/serializers.py

from marshmallow import Schema, fields
from sqlalchemy.orm import class_mapper
from sqlalchemy import Table, Integer, String, DateTime, Float, Boolean, Date
import datetime

# Словарь для сопоставления типов SQLAlchemy и Marshmallow
SQLALCHEMY_TYPE_MAPPING = {
    Integer: fields.Int,
    String: fields.Str,
    DateTime: fields.DateTime,
    Float: fields.Float,
    Boolean: fields.Bool,
    Date: fields.Date,
}

def get_field_class(column_type):
    """Возвращает соответствующий класс поля Marshmallow на основе типа SQLAlchemy."""
    for sqlalchemy_type, marshmallow_field in SQLALCHEMY_TYPE_MAPPING.items():
        if isinstance(column_type, sqlalchemy_type):
            return marshmallow_field
    return fields.Str  # По умолчанию строковое поле

class UniversalSerializer(Schema):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем поля на основе модели
        if isinstance(model, Table):
            columns = model.columns
        else:
            columns = class_mapper(model).columns
        
        for column in columns:
            field_class = get_field_class(column.type)
            self.dump_fields[column.name] = field_class(attribute=column.name)
            # Handle date fields by converting them properly if they are strings
            if field_class == fields.Date:
                self.dump_fields[column.name] = fields.Method(
                    serialize=lambda obj: obj[column.name].isoformat() if isinstance(obj[column.name], (datetime.date, datetime.datetime)) else obj[column.name],
                    attribute=column.name
                )
        