def apply_transformation(value, transformation):
    if transformation == 'function_name':
        return custom_transformation_function(value)
    # Можно добавить дополнительные преобразования
    return value

def custom_transformation_function(value):
    # Пример пользовательской функции
    return value.upper()
