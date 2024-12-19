# app/controllers/base_controller.py

from sqlalchemy.inspection import inspect
from settings import UPLOAD_DIR
from werkzeug.utils import secure_filename
import os
import uuid
import pandas as pd

from app.utils.functions import apply_transformation
from app.utils.metadata import MetadataManager
from app.repositories.base_repository import BaseRepository
from logging_config import logger

_cache = {}
class BaseController:

    def __init__(self, repository):
        self.repo = repository
        self.metadata_manager = MetadataManager()
        self.allowed_extensions_for_load_table = {'csv', 'xlsx'}
        self.allowed_extensions_for_mediafile = {'jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi'}
        #self._cache = {}  # Кэш запросов

    def get_combined_metadata(self):
        """Получить комбинированные метаданные"""
        db_metadata = self.repo.get_table_metadata()
        table_name = db_metadata['schema'] + '_' + db_metadata['table_name']

        
        json_metadata = self.metadata_manager.get_metadata(table_name) # Получение метаданных из JSON-файла
        json_columns_map = {column['name']: column for column in json_metadata.get('columns', [])}

        combined_columns = []
        for db_column in db_metadata['columns']:
            json_column = json_columns_map.get(db_column['name'], {})
            combined_column = db_column | json_column  # Объединение метаданных из БД и JSON

            combined_columns.append(combined_column)

        combined_metadata = {
            "table_name": table_name,
            "columns": combined_columns
        }

        return combined_metadata

    def get_page(self, offset, limit):
        """Получить страницу записей"""
        return self.repo.get_page(offset, limit)
    
    def get_count(self):
        """Получить количество записей"""
        return self.repo.get_count()


    def sort (self, **kwargs):
        """Сортировка"""
        return self.repo.sort_by_fields(**kwargs)

    def get_by_id(self, entity_id):
        """Получить запись по ID"""
        return self.repo.get_by_id(entity_id)
    
    def filter_records(self, **filters):
        """Получить отфильтрованные данные"""
        return self.repo.filter_by_fields(**filters)

    def search(self, query):
        """Поиск по строке"""
        return self.repo.search(query)

    def create_record(self, data, table):
        """Создать новую запись"""
        data = self.from_dict (table, data)
        return self.repo.add(data)

    def update_record(self, record_id, data):
        """Обновить существующую запись"""
        record = self.repo.get_by_id(record_id)
        if record:
            return self.repo.update(record, data)
        return None

    def delete_record(self, record_id):
        """Удалить запись"""
        record = self.repo.get_by_id(record_id)
        if record:
            self.repo.delete(record)
            return True
        return False
    
    @staticmethod
    def to_dict(self, obj):
        """Преобразует объект модели в словарь"""
        return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}
    
    def from_dict(self, table_name: str, data: dict):
        """
        Универсальный метод для создания экземпляра модели на основе названия таблицы и данных.
        """
        # Получаем класс модели по имени таблицы
        model_class = BaseRepository.get_model_by_table_name(table_name)

        # Создаем пустой экземпляр модели
        model_instance = model_class()

        # Получаем список всех колонок модели
        mapper = inspect(model_class)

        # Заполняем поля модели значениями из словаря data
        for column in mapper.attrs:
            column_name = column.key
            if column_name in data:
                setattr(model_instance, column_name, data[column_name])

        return model_instance
    
    def __allowed_file(self, filename: str, filetype: str):
        """Проверка разрешенного файла"""
        if filetype == 'data':
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions_for_load_table
        elif filetype == 'media':
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions_for_mediafile


    def upload_file(self, file, filetype = 'media'):
        """Загрузить файл на сервер"""
        if file and self.__allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_id = str(uuid.uuid4())  # Генерация уникального идентификатора для файла
            file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{filename}")
            file.save(file_path)
            return file_id
        return None
    
    def transform_file(self, file):
        '''Преобразование загруженного файла данных по мапингу'''
        # Определяем формат файла
        try:
            if file.filename.endswith('.csv'):
                data = pd.read_csv(file, delimiter=';')
            elif file.filename.endswith(('.xls', '.xlsx')):
                data = pd.read_excel(file)
            else:
                return {"status": "fail", "message": "Unsupported file format"}, 400
        except Exception as e:
            logger.error(f'Ошибка: {e}')
            return {"status": "fail", "message": f"Error reading file: {e}"}, 400

        # Убираем пробелы и символы перевода строк в текстовых данных
        def clean_string(value):
            if isinstance(value, str):
                return value.strip()  # Удаляем пробелы, табуляции и переводы строк
            return value  # Возвращаем значение без изменений, если это не строка
        
        # Применяем функцию очистки ко всем ячейкам датафрейма
        data = data.applymap(clean_string)

        # Преобразуем NaN и NaT в None
        data = data.where(pd.notna(data), None)
        
        # Конвертируем данные в формат словаря
        data = data.to_dict(orient='records')
        try:
            mapped_data = self.apply_mapping(data)
            return mapped_data
        except Exception as e:
            print(e)# Выводим ошибку
            return {"status": "fail", "message": f"Error mapping data: {e}"}, 400


    def apply_mapping(self, data, function_object = None):
        """Применение маппинга к данным с преобразованием типов"""
        from app.utils.helpers import create_service, get_value_by_path
        metadata = self.get_combined_metadata()
        # Применяем маппинг и преобразования
        transformed_data = []
        
        # Функция для приведения типов
        def convert_to_type(value, column_type):
            if value is None:
                return None
            if pd.isna(value):
                return None
            try:
                if column_type.lower() in { 'integer', 'int', 'smallint', 'bigint'}:
                    return int(value)
                elif column_type.lower() in { 'float', 'double', 'money', 'smallmoney'}:
                    return float(value)
                elif column_type.lower() in { 'string', 'varchar', 'text', 'jsonb'}:
                    return str(value)
                elif column_type.lower() in { 'bool', 'boolean'}:
                    return bool(value)
                # Добавляем другие типы данных при необходимости
                else:
                    return value
            except (ValueError, TypeError):
                # Обработка ошибок приведения типов, например, возвращаем значение как есть или None
                return None

        try:
            if function_object:
                if function_object.__class__.__name__ == 'OzonTransfomationFunctions':
                    mapkey = 'mappings_json_ozon'
                elif function_object.__class__.__name__ == 'WBTransformationFunctions':
                    mapkey = 'mappings_json_wb'
            else:
                mapkey = 'mappings'
            for row in data:
                transformed_row = {}
                for col_meta in metadata['columns']:
                    source_column = col_meta[mapkey].get('import_name', None)
                    transformation = col_meta[mapkey].get('transformation', 'direct')
                    additional_fields = col_meta[mapkey].get('additional_fields', [])
                    column_type = col_meta.get('type', 'string')  # Получаем тип данных из метаданных

                    if transformation == 'skip':
                        continue
                    elif transformation == 'direct':
                        # Прямое сопоставление с преобразованием типа
                        transformed_row[col_meta['name']] = convert_to_type(get_value_by_path(row, source_column), column_type)
                    elif transformation == 'db_get_key_from_fields':
                        # Применение функции преобразования с обращением к базе данных
                        if col_meta.get('foreign_key'):
                            table_name = col_meta['foreign_key'].get('target_table')
                            if table_name:
                                service = create_service(table_name)
                                field_name = col_meta['foreign_key'].get('lookup_field','name')
                                key_name =  col_meta['foreign_key'].get('key_field','id')
                                pseudonym = col_meta['foreign_key'].get('pseudonym')
                                value = str(get_value_by_path(row, source_column))   
                                transformed_value = apply_transformation(
                                    value, transformation, service=service, field_name = field_name, key_name = key_name, pseudonym = pseudonym
                                    )
                                transformed_row[col_meta['name']] = convert_to_type(transformed_value, column_type)
                    elif transformation == 'get_ozon_client_phone':
                        posting_number = get_value_by_path(row, 'posting_number')
                        if posting_number:
                            value = get_value_by_path(row, source_column)
                            transformed_value = apply_transformation(value, transformation, func_obj=function_object, posting_number = posting_number)
                            transformed_row[col_meta['name']] = convert_to_type(transformed_value, column_type)
                    else:
                        # Применение функции преобразования с последующим приведением типа
                        kwargs = {}
                        for field in additional_fields:
                            val = get_value_by_path(row, field)
                            key = field.split('.')[-1]
                            kwargs[key] = val
                        transformed_value = apply_transformation(get_value_by_path(row, source_column), transformation, func_obj=function_object, **kwargs)
                        transformed_row[col_meta['name']] = convert_to_type(transformed_value, column_type)
                
                transformed_data.append(transformed_row)
                #print(len(transformed_data))
        except Exception as e:
            logger.error(f'Ошибка {e}')

        # Передаем данные в репозиторий для сохранения
        return transformed_data

    
    def load_transformed_data(self, file):
        """Загрузка преобразованных данных в БД"""
        data = self.transform_file(file)
        if isinstance(data, dict):
            return data
        else:
            try:
                self.repo.save_import_data_to_table(data)
            except Exception as e:
                print (e)
                return {"status": "fail", "message": f"Error saving data: {e}"}, 400
            return {"status": "success", "message": "Data saved successfully"}, 200

    def get_key_from_fields(self, **kwargs):
        """Получить значение ключа по значениям полей"""
        # Формируем ключ для кэша на основе входных данных
        cache_key = f"{kwargs.get('field_name')}_{kwargs.get('value')}"
        cache_key_p = f"{kwargs.get('pseudonym')}_{kwargs.get('value')}"
        # Проверяем, есть ли результат в кэше
        if cache_key in _cache:
            return _cache[cache_key]

        if cache_key_p in _cache:
            return _cache[cache_key_p]

        field_name = kwargs.get('field_name')
        key_name = kwargs.get('key_name')
        value = kwargs.get('value')
        pseudonym = kwargs.get('pseudonym')

        # Выполняем запросы к базе данных
        rows = self.repo.find_by_name(field_name, value)

        if rows:
            result = getattr(rows[0], key_name)
            _cache[cache_key] = result
        else:
            if pseudonym:
                rows = self.repo.find_by_name_in_array(pseudonym, value)
                if rows:
                    result = getattr(rows[0], key_name)
                    _cache[cache_key_p] = result
                else:
                    result = None
            else:
                result = None
        # Сохраняем результат в кэш
        return result

    



