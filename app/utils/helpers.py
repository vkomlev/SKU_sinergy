# app/utils/helpers.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import DATABASE

def get_engine():
    return create_engine(f"{DATABASE['drivername']}://{DATABASE['username']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['database']}")

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

