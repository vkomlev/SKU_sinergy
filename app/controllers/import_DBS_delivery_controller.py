# app/controllers/import_DBS_delivery_controller.py

from app.controllers.base_controller import BaseController
from app.repositories.import_DBS_delivery_repository import ImportDBSDeliveryRepository

class ImportDBSDeliveryController(BaseController):
    def __init__(self, session):
        repo = ImportDBSDeliveryRepository(session)
        super().__init__(repo)

    def get_page(self, offset, limit, sort_by, sort_order):
        return super().get_page(offset, limit, sort_by, sort_order)
