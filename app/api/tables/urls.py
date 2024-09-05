# app/api/tables/urls.py

from flask import Blueprint
from app.api.tables.views import get_import_DBS_delivery_view

tables_api = Blueprint('tables_api', __name__)

# Регистрация маршрутов через Blueprint
def setup_my_routes(app): 
    tables_api.add_url_rule('/api/tables/import_DBS_delivery/data', 'import_DBS_delivery', get_import_DBS_delivery_view)
    app.register_blueprint(tables_api)