# app/repositories/base_repository.py

from sqlalchemy.orm import Session
from app.model_import import DBSDelivery

class BaseRepository:
    def __init__(self, model, session: Session):
        """Передаем при создании  экземпляра модель данных и сессию подключения"""
        self.model = model
        self.session = session

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
    

    def get_page(self, offset, limit):
        query = self.session.query(self.model)
        query = query.limit(limit).offset(offset)
        return query.all()

    def sort_by_fields(self, **kwargs):
        query = self.session.query(self.model)
        for field, direction in kwargs.items():
            field_name, order = direction.split()
            column = getattr(self.model, field_name)
            if order.upper() == "ASC":
                query = query.order_by(column.asc())
            elif order.upper() == "DESC":
                query = query.order_by(column.desc())
            else:
                raise ValueError(f"Invalid sort direction: {order}")
        return query.all()


    def get_by_fields(self, **kwargs):
        """Получить записи по значениям полей, переданным через kwargs"""
        query = self.session.query(self.model)
        for key, value in kwargs.items():
            query = query.filter(getattr(self.model, key) == value)
        return query.all()



