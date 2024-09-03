# app/main/__init__.py

from flask import Flask
#from .urls import setup_routes
from app.api.tables.urls import setup_my_routes

def create_app():
    app = Flask(__name__)

    # Настройка маршрутов
    setup_my_routes(app)
    
    return app