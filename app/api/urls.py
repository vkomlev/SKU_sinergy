from app.api.views import upload_file, upload_to_table
from flask import Blueprint

# Добавляем маршрут для загрузки файла
api = Blueprint('tables_api', __name__)

def  setup_root_api_routes(app): 
    app.add_url_rule('/api/upload', view_func=upload_file, methods=['POST'])
    app.add_url_rule('/api/upload/<table_name>', view_func=upload_to_table, methods=['POST'])
