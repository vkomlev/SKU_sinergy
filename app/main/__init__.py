# app/main/__init__.py

from flask import Flask
#from app.main import setup_routes  # Это регистрация маршрутов для главной страницы
from app.api.tables.urls import setup_table_api_routes  # Это регистрация маршрутов для API
from app.api.urls import setup_root_api_routes
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # Разрешаем запросы с вашего frontend (localhost:3000)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    # Регистрация маршрутов для главной страницы, заказов и доставки
    #setup_routes(app)

    # Регистрация маршрутов API через Blueprint
    setup_root_api_routes(app)
    setup_table_api_routes(app)
    
    return app
