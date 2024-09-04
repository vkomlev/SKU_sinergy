# app/repositories/import_DBS_delivery_repository.py

from app.model_import import DBSDelivery
from app.repositories.base_repository import BaseRepository

class ImportDBSDeliveryRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(DBSDelivery, session)