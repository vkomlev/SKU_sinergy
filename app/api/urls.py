from app.api.views import (
        upload_file, 
        upload_to_table, 
        r_script, 
        calculate_distance, 
        mkad_distance,
        ozon_dbs_api_load,
        wb_dbs_api_load
        )
from flask import Blueprint

# Добавляем маршрут для загрузки файла
api = Blueprint('tables_api', __name__)

def  setup_root_api_routes(app): 
    app.add_url_rule('/api/upload', view_func=upload_file, methods=['POST']) #Загрузить произвольный файл
    app.add_url_rule('/api/upload/<table_name>', view_func=upload_to_table, methods=['POST']) #Загрузить файл в таблицу БД
    app.add_url_rule('/api/run-r-script', view_func=r_script, methods=['POST']) #Выполнить R скрипт
    app.add_url_rule('/api/get_distance', view_func=calculate_distance, methods=['POST'])  # Расчет расстояний между двумя адресами
    app.add_url_rule('/api/mkad_distance', view_func=mkad_distance, methods=['POST']) #Расчет расстояний от МКАД до адреса/координат
    app.add_url_rule('/api/ozon/dbs_load', view_func=ozon_dbs_api_load, methods=['POST']) #Загрузка отправлений ОЗОН
    app.add_url_rule('/api/wb/dbs_load', view_func=wb_dbs_api_load, methods=['POST']) #Загрузка отправлений ОЗОН
