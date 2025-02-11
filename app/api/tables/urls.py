# app/api/tables/urls.py

from flask import Blueprint
from app.api.tables.views import get_data_view, get_metadata_view, search, create_record, update_record, delete_record, get_record

tables_api = Blueprint('tables_api', __name__)

# Регистрация маршрутов через Blueprint
def setup_table_api_routes(app): 
    tables_api.add_url_rule('/api/tables/<table_name>/data', 'data', get_data_view)
    tables_api.add_url_rule('/api/tables/<table_name>/metadata', 'metadata', get_metadata_view)
    tables_api.add_url_rule('/api/tables/<table_name>/search', 'search', search)
    tables_api.add_url_rule('/api/tables/<table_name>/records', 'create_record', create_record, methods=['POST'])
    tables_api.add_url_rule('/api/tables/<table_name>/records/<int:record_id>', 'update_record', update_record, methods=['PUT'])
    tables_api.add_url_rule('/api/tables/<table_name>/records/<int:record_id>', 'delete_record', delete_record, methods=['DELETE'])
    tables_api.add_url_rule('/api/tables/<table_name>/records/<int:record_id>', 'get_record', get_record, methods=['GET'])
    app.register_blueprint(tables_api)