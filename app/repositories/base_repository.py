# app/repositories/base_repository.py

from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.model_import import DBSDelivery
from sqlalchemy.inspection import inspect
from app.utils.metadata import MetadataManager


class BaseRepository:
    def __init__(self, model, session: Session):
        """Передаем при создании  экземпляра модель данных и сессию подключения"""
        self.model = model
        self.session = session
        self.__temp_query = None
        self.metadata_manager = MetadataManager()

    def add(self, entity):
        """Добавить запись"""
        self.session.add(entity)
        self.session.commit()
        return entity

    def delete(self, entity):
        """Удалить запись"""
        self.session.delete(entity)
        self.session.commit()

    def update(self):
        """Обновить запись"""
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
        #return self.model.__table__.primary_key.columns.keys()[0]
    
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
        filter_criteria = filters.get('filters', filters)
        
        if filter_criteria:
            for column_name, value in filter_criteria.items():
                query = query.filter(getattr(self.model, column_name) == value)
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
        table_name = self.model.__tablename__

        columns_info = []

        for column in inspector.columns: #cтолбцы таблицы из бд
            column_info = {
                'name':column.name,
                'type':str(column.type),
                'primary_key':column.primary_key,
                'foreign_key': None
            }

            if column.foreign_keys: #внешние ключи
                for fk in column.foreing_keys:
                    column_info['foreign_key'] = {
                        'target_table': fk.column.table.name,
                        'target_column': fk.column.name
                    }
            
            columns_info.append(column_info) #добавление столбцов из бд

        db_metadata = {"table_name":self.model.__tablename__,
                       "columns": columns_info}

        table_name = db_metadata['table_name']
        json_metadata = self.metadata_manager.get_metadata(table_name)
        json_columns_map = {column['name']:column for column in json_metadata.get('columns', [])}

        combined_columns = [] 

        for db_column in db_metadata['columns']: #объединение метаданных из бд и json
            json_column = json_columns_map.get(db_column['name'], {})
            combined_column = db_column | json_column
            combined_columns.append(combined_column)

        combined_metadata = {
            "table_name": table_name,
            "columns": combined_columns
        }
        
        return combined_metadata
    
    def search(self, query):
        """Поиск по строке query"""
        if not query: #Если параметр не задан, возвращается пустой список
            return []
        
        columns = self.model.__table__.columns
        
        param_check = [column.ilike(f"%{query}%") for column in columns if column.type.python_type == str] #поиск по параметру
        results = self.session.query(self.model).filter(or_(*param_check)).all() #фильтрует заказы по условию
        return results
    