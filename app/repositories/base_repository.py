# app/repositories/base_repository.py

from sqlalchemy.orm import Session

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

    def get_by_id(self, entity_id):
        """Получить запись по ID"""
        return self.session.query(self.model).get(entity_id)

    def get_all(self):
        """Получить все записи"""
        return self.session.query(self.model).all()

    def get_page(self, offset, limit):
        """Получить страницу записей с offset по limit"""
        return self.session.query(self.model).offset(offset).limit(limit).all()

    def get_by_fields(self, **kwargs):
        """Получить записи по значениям полей, переданным через kwargs"""
        query = self.session.query(self.model)
        for key, value in kwargs.items():
            query = query.filter(getattr(self.model, key) == value)
        return query.all()