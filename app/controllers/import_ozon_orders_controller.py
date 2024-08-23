# app/controllers/import_ozon_orders_controller.py

from app.controllers.base_controller import BaseController
from app.repositories.import_ozon_orders_repository import ImportOzonOrderRepository

class ImportOzonOrdersController(BaseController):
    def __init__(self, session):
        repo = ImportOzonOrderRepository(session)
        super().__init__(repo)
