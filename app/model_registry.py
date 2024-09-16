# app/model_registry.py

model_registry = {}

def register_model(model):
    table_name = model.__tablename__
    schema = model.__table_args__.get('schema') if hasattr(model, '__table_args__') else None
    
    if schema:
        table_name = f"{schema}.{table_name}"  # Учитываем схему
    
    model_registry[table_name.lower()] = model

def get_model_by_table_name(table_name):
    model = model_registry.get(table_name.lower())
    if model is None:
        raise ValueError(f"Модель для таблицы '{table_name}' не найдена.")
    return model
