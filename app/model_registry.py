# app/model_registry.py
from sqlalchemy import Table

model_registry = {}

def register_model(model):
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
    from app.model_import import DBSDelivery, OrdersOzon
    from app.model_main import Products

    model = model_registry.get(table_name.lower())
    if model is None:
        raise ValueError(f"Модель для таблицы '{table_name}' не найдена.")
    return model
