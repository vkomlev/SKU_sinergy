# app/repositories/base_repository.py

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.model_registry import get_model_by_table_name
from sqlalchemy.inspection import inspect
from app.utils.metadata import MetadataManager


class BaseRepository:
    def __init__(self, model, session: Session):
        """Передаем при создании  экземпляра модель данных и сессию подключения"""
        self.model = model
        self.session = session
        self.__temp_query = None
        self.metadata_manager = MetadataManager()
    
    @staticmethod
    def get_model_by_table_name(table_name: str):
        """
        Универсальный метод для поиска класса модели по имени таблицы с использованием рефлексии.
        """
        return get_model_by_table_name(table_name)

    def add(self, entity):
        """Добавить запись"""
        self.session.add(entity)
        self.session.commit()
        return entity
    
    def update(self, entity, data):
        """Обновить запись"""
        for key, value in data.items():
            setattr(entity, key, value)
        self.session.commit()
        return entity
    
    def delete(self, entity):
        """Удалить запись"""
        self.session.delete(entity)
        self.session.commit()

    def get_all(self):
        """Получить все записи"""
        return self.session.query(self.model).all()

    def get_by_id(self, entity_id):
        """Получить запись по ID"""
        return self.session.query(self.model).get(entity_id)
    
    def get_primary_key_name(self):
        """Получить название первичного ключа для модели"""
        primary_key_column = self.model.__table__.primary_key.columns.keys()[0]
        return primary_key_column
    
    def __get_query(self):
        if self.__temp_query:
            return self.__temp_query
        return self.session.query(self.model)

    def get_count(self):
        """Получить количество записей"""
        return self.__get_query().count()

    def get_page_count(self, limit):
        """Получить количество страниц"""
        return (self.get_count() + limit - 1) // limit

    def get_page(self, offset, limit):
        query = self.__get_query()
        return query.offset(offset).limit(limit).all()

    def filter_by_fields(self, **filters):
        query = self.__get_query()
        # Проверяем наличие фильтров и корректируем на случай, если они вложены
        filters = filters.get('filters', filters)
        for item in filters:
            if item.get('column'):
                if item.get('expression') == '=':
                    query = query.filter(getattr(self.model, item.get('column')) == item.get('value'))
        self.__temp_query = query
        return query.all() 

    def sort_by_fields(self, **kwargs):
        query = self.__get_query()
        for field, direction in kwargs.items():
            field_name, order = direction.split()
            column = getattr(self.model, field_name)
            if order.upper() == "ASC":
                query = query.order_by(column.asc())
            elif order.upper() == "DESC":
                query = query.order_by(column.desc())
            else:
                raise ValueError(f"Invalid sort direction: {order}")
        self.__temp_query = query
        return query.all()

    def get_by_fields(self, **kwargs):
        """Получить записи по значениям полей, переданным через kwargs"""
        query = self.session.query(self.model)
        for key, value in kwargs.items():
            query = query.filter(getattr(self.model, key) == value)
        return query.all()
    
    def get_table_metadata(self):
        """Получить комбинированные метаданные таблицы"""
        inspector = inspect(self.model)
        columns_info = []

        for column in inspector.columns: # Столбцы таблицы из БД
            column_info = {
                'name':column.name,
                'type':str(column.type),
                'primary_key':column.primary_key,
                'foreign_key': None
            }

            if column.foreign_keys: # Внешние ключи
                for fk in column.foreing_keys:
                    column_info['foreign_key'] = {
                        'target_table': fk.column.table.name,
                        'target_column': fk.column.name
                    }
            
            columns_info.append(column_info) # Добавление столбцов из БД
        args = self.model.__table_args__ if hasattr(self.model, '__table_args__') else None
        if args:
            schema = args[-1].get('schema') if isinstance(args, tuple) else args.get('schema','public')
        db_metadata = {"table_name":self.model.__tablename__,
                       "schema":schema,
                       "columns": columns_info}

        return db_metadata # Возвращаем метаданные только из БД
    
    def search(self, query):
        """Поиск по строке query"""
        if not query: #Если параметр не задан, возвращается пустой список
            return []
        
        columns = self.model.__table__.columns
        
        param_check = [column.ilike(f"%{query}%") for column in columns if column.type.python_type == str] #поиск по параметру
        results = self.session.query(self.model).filter(or_(*param_check)).all() #фильтрует заказы по условию
        return results
    


    def save_import_data_to_table(self, data):
        '''Импорт данных в таблицу БД'''
        metadata = MetadataManager()
        # Получаем название уникального ключа для таблицы
        key_names = metadata.get_unique_columns(self.model.__tablename__)

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