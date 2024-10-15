# app/utils/helpers.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import DATABASE
from app.services.base_service import BaseService
from app.repositories.base_repository import BaseRepository
from app.controllers.base_controller import BaseController

def get_engine():
    return create_engine(f"{DATABASE['drivername']}://{DATABASE['username']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['database']}")

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

def create_service(table_name, **kwargs):
    session = get_session()
    model = BaseRepository.get_model_by_table_name(table_name.replace('_', '.', 1))
    service = BaseService(BaseController(BaseRepository(model, session)))
    return service
