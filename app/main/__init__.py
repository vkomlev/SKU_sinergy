# app/main/__init__.py

from flask import Flask
from .urls import setup_routes  # Это регистрация маршрутов для главной страницы
from app.api.tables.urls import setup_my_routes  # Это регистрация маршрутов для API

def create_app():
    app = Flask(__name__)

    # Регистрация маршрутов для главной страницы, заказов и доставки
    setup_routes(app)

    # Регистрация маршрутов API через Blueprint
    setup_my_routes(app)
    
    return app
