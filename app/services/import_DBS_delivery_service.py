# app/services/import_DBS_delivery_service.py
from app.services.base_service import BaseService
from app.controllers.import_DBS_delivery_controller import ImportDBSDeliveryController


class ImportDBSDeliveryService(BaseService):
    def __init__(self, session):
        controller = ImportDBSDeliveryController(session)
        super().__init__(controller)