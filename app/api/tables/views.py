#app/api/tables/views.py

from flask import render_template, request, jsonify
from app.utils.helpers import get_session
from app.services.import_DBS_delivery_service import ImportDBSDeliveryService
from app.model_import import DBSDelivery
from app.api.tables.serializers import UniversalSerializer
from app.services.import_ozon_orders_service import ImportOzonOrdersService

def get_import_DBS_delivery_view():
    session = get_session()
    delivery_service = ImportDBSDeliveryService(session)
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    deliveries = delivery_service.get_with_pagination(page, per_page)

    serializer = UniversalSerializer(DBSDelivery, many = True)
    deliveries_data = serializer.dump(deliveries)

    json_data = {
        'page': page,
        'total': len(deliveries_data),
        'deliveries': deliveries_data

    }

    return jsonify(json_data)