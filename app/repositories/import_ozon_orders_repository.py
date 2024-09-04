# app/repositories/import_ozon_orders_repository.py

from app.model_import import OrdersOzon
from app.repositories.base_repository import BaseRepository

class ImportOzonOrderRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(OrdersOzon, session)