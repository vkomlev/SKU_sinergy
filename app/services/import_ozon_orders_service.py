# app/services/import_ozon_orders_service.py

from app.services.base_service import BaseService
from app.controllers.import_ozon_orders_controller import ImportOzonOrdersController

class ImportOzonOrdersService(BaseService):
    def __init__(self, session):
        controller = ImportOzonOrdersController(session)
        super().__init__(controller)