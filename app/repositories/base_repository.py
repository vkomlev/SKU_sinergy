# app/repositories/base_repository.py

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, Table, any_
from app.model_registry import get_model_by_table_name
from sqlalchemy.inspection import inspect
from app.utils.metadata import MetadataManager
import time
from sqlalchemy.exc import OperationalError

def retry_on_failure(retries=5, delay=2):
    """Декоратор для повторных попыток при сбоях подключения"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except OperationalError as e:
                    attempts += 1
                    print(f"Попытка {attempts} из {retries} не удалась: {e}")
                    if attempts < retries:
                        print(f"Повтор через {delay} секунд...")
                        time.sleep(delay)
                    else:
                        print("Все попытки исчерпаны.")
                        raise
        return wrapper
    return decorator

def manage_session(func):
    """Декоратор для автоматического закрытия сессии SQLAlchemy"""
    def wrapper(self, *args, **kwargs):
        try:
            # Выполняем основную функцию
            result = func(self, *args, **kwargs)
            # Возвращаем результат
            return result
        except Exception as e:
            # В случае ошибки откатываем транзакцию
            self.session.rollback()
            raise e
        finally:
            # Закрываем сессию после использования
            self.session.close()
    return wrapper


class BaseRepository:
    def __init__(self, model, session: Session):
        """Передаем при создании  экземпляра модель данных и сессию подключения"""
        self.model = model
        self.session = session
        self.__temp_query = None
        self.metadata_manager = MetadataManager()
    
    @staticmethod
    @retry_on_failure(retries=5, delay=2)
    def get_model_by_table_name(table_name: str):
        """
        Универсальный метод для поиска класса модели по имени таблицы с использованием рефлексии.
        """
        return get_model_by_table_name(table_name)
    
    @retry_on_failure(retries=5, delay=2)
    #@manage_session
    def add(self, entity):
        """Добавить запись"""
        self.session.add(entity)
        self.session.commit()
        return entity
    
    @retry_on_failure(retries=5, delay=2)
    #@manage_session
    @retry_on_failure(retries=5, delay=2)
    def update(self, entity, data):
        """Обновить запись"""
        # Привязать entity к сессии, если он не был загружен с этой сессии
        if self.session.object_session(entity) is None:
            self.session.add(entity)  # Привязка объекта к сессии, если это необходимо
            
        for key, value in data.items():
            setattr(entity, key, value)

        self.session.commit()
        return entity

    
    @retry_on_failure(retries=5, delay=2)
    #@manage_session
    def delete(self, entity):
        """Удалить запись"""
        self.session.delete(entity)
        self.session.commit()

    @retry_on_failure(retries=5, delay=2)
    @manage_session
    def get_all(self):
        """Получить все записи"""
        return self.session.query(self.model).all() if isinstance(self.model, Table) else self.__get_query().all()
    @retry_on_failure(retries=5, delay=2)
    @manage_session
    def get_by_id(self, entity_id):
        """Получить запись по ID"""
        return self.__get_query().get(entity_id) if hasattr(self.model, '__tablename__') else self.session.query(self.model).get(entity_id)
    
    @retry_on_failure(retries=5, delay=2)
    @manage_session
    def get_primary_key_name(self):
        """Получить название первичного ключа для модели"""
        primary_key_column = self.model.primary_key.columns.keys()[0] if isinstance(self.model, Table) else self.model.__table__.primary_key.columns.keys()[0]
        return primary_key_column
    
    @retry_on_failure(retries=5, delay=2)
    @manage_session
    def __get_query(self):
        if self.__temp_query:
            return self.__temp_query
        return self.session.query(self.model)

    @retry_on_failure(retries=5, delay=2)
    @manage_session
    def get_count(self):
        """Получить количество записей"""
        return self.__get_query().count()

    @retry_on_failure(retries=5, delay=2)
    @manage_session
    def get_page_count(self, limit):
        """Получить количество страниц"""
        return (self.get_count() + limit - 1) // limit

    @retry_on_failure(retries=5, delay=2)
    @manage_session
    def get_page(self, offset, limit):
        query = self.__get_query()
        return query.offset(offset).limit(limit).all()

    @retry_on_failure(retries=5, delay=2)
    @manage_session
    def filter_by_fields(self, **filters):
        query = self.__get_query()
        filters = filters.get('filters', filters)
        for item in filters:
            if item.get('column'):
                column = self.get_column(item.get('column'))
                if item.get('expression') == '=':
                    query = query.filter(column == item.get('value'))
        self.__temp_query = query
        return query.all()

    @retry_on_failure(retries=5, delay=2)
    @manage_session
    def sort_by_fields(self, **kwargs):
        query = self.__get_query()
        for field, direction in kwargs.items():
            field_name, order = direction.split()
            column = self.get_column(field_name)
            if order.upper() == "ASC":
                query = query.order_by(column.asc())
            elif order.upper() == "DESC":
                query = query.order_by(column.desc())
            else:
                raise ValueError(f"Invalid sort direction: {order}")
        self.__temp_query = query
        return query.all()

    @retry_on_failure(retries=5, delay=2)
    @manage_session
    def get_by_fields(self, **kwargs):
        query = self.session.query(self.model)
        for key, value in kwargs.items():
            column = self.get_column(key)
            query = query.filter(column == value)
        return query.all()
    
    @retry_on_failure(retries=5, delay=2)
    @manage_session
    def find_by_name(self, name_column, name_value):
        """Поиск записи по имени"""
        return self.session.query(self.model).filter(getattr(self.model, name_column) == name_value).all()
    
    @retry_on_failure(retries=5, delay=2)
    @manage_session
    def find_by_name_in_array(self, name_column, name_value):
        """Поиск записи, когда поле является массивом строк (PostgreSQL)"""
        # Получаем колонку через getattr
        column = getattr(self.model, name_column)
        
        # Используем правильный синтаксис PostgreSQL для поиска по массиву
        return self.session.query(self.model).filter(name_value == any_(column)).all()
    
    @staticmethod
    def get_full_table_name(model):
        '''Get full table name from model'''
        if isinstance(model, Table):
            schema = model.schema if model.schema else 'public'
            table_name = model.name
        else:
            args = model.__table_args__ if hasattr(model, '__table_args__') else None
            schema = 'public'
            if args:
                schema = args[-1].get('schema') if isinstance(args, tuple) else args.get('schema', 'public')
            table_name = model.__tablename__
        
        return f"{schema}.{table_name}", schema, table_name
    
    @retry_on_failure(retries=5, delay=2)
    @manage_session
    def get_table_metadata(self):
        """Get combined metadata for the table"""
        inspector = inspect(self.model)

        if isinstance(self.model, Table):
            columns = self.model.columns
        else:
            columns = inspector.columns

        columns_info = []
        full, schema, tablename = self.get_full_table_name(self.model)
        for column in columns:  # Columns from the database table
            column_info = {
                'name': column.name,
                'type': str(column.type),
                'primary_key': column.primary_key if hasattr(column, 'primary_key') else False,
                'foreign_key': None
            }

            if column.foreign_keys:  # Foreign keys
                for fk in column.foreign_keys:
                    column_info['foreign_key'] = {
                        'target_table': schema + '_' + fk.column.table.name,
                        'target_column': fk.column.name
                    }
            
            columns_info.append(column_info)  # Add columns from DB
        
        db_metadata = {
            "table_name": tablename,
            "schema": schema,
            "full_table_name": full,
            "columns": columns_info
        }

        return db_metadata  # Return metadata from DB only

    @retry_on_failure(retries=5, delay=2)
    @manage_session
    def search(self, query):
        """Поиск по строке query"""
        if not query:
            return []
        columns = self.model.columns if isinstance(self.model, Table) else self.model.__table__.columns
        param_check = [column.ilike(f"%{query}%") for column in columns if column.type.python_type == str]
        results = self.session.query(self.model).filter(or_(*param_check)).all()
        return results
    

    #@retry_on_failure(retries=5, delay=2)
    #@manage_session
    def save_import_data_to_table(self, data):
        '''Импорт данных в таблицу БД'''
        metadata = MetadataManager()
        # Получаем название уникального ключа для таблицы
        full_name = self.get_full_table_name(self.model)[0]
        key_names = metadata.get_unique_columns(full_name)

        for row in data:
            # Извлекаем значения уникальных полей
            keys = {}
            for key in key_names:
                keyname = key.get('name')
                if keyname:
                    keys[keyname] = row.get(keyname)

            if keys:
                # Проверяем, существует ли запись с данным значением первичного ключа
                entity = self.get_by_fields(**keys)
                if entity:
                    # Если запись существует, обновляем её
                    self.update(entity[0], row)
                else:
                    # Если записи нет, создаем новую запись
                    new_entity = self.model(**row)
                    self.add(new_entity)
            else:
                # Если нет значения первичного ключа, создаем новую запись
                new_entity = self.model(**row)
                self.add(new_entity)
    
    def get_column(self, column_name):
        if isinstance(self.model, Table):
            return self.model.columns.get(column_name)
        return getattr(self.model, column_name)