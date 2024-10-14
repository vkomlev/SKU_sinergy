from app.services.base_service import BaseService
def apply_transformation(value, transformation, **kwargs):
    if transformation == 'db_get_key_from_fields':
        service = kwargs.get('service')
        if service:
            return service.get_key_from_fields(value=value, **kwargs)
    # Можно добавить дополнительные преобразования
    return value

def custom_transformation_function(value):
    # Пример пользовательской функции
    return value.upper()
