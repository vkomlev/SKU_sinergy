# app/main/__init__.py

from flask import Flask
from .urls import setup_routes  # Это регистрация маршрутов для главной страницы
from app.api.tables.urls import setup_my_routes  # Это регистрация маршрутов для API
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # Разрешаем запросы с вашего frontend (localhost:3000)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    # Регистрация маршрутов для главной страницы, заказов и доставки
    setup_routes(app)

    # Регистрация маршрутов API через Blueprint
    setup_my_routes(app)
    
    return app
