#app/api/tables/views.py

import json
from flask import render_template, request, jsonify
from app.utils.helpers import get_session
from app.services.import_DBS_delivery_service import ImportDBSDeliveryService
from app.model_import import DBSDelivery
from app.api.tables.serializers import UniversalSerializer
from app.services.import_ozon_orders_service import ImportOzonOrdersService

def get_import_DBS_delivery_view():
    session = get_session()
    delivery_service = ImportDBSDeliveryService(session)
    
    page = request.args.get('page', default= 1, type=int)
    size = request.args.get('size', default= 25, type=int)

    sort_params = {key: value for key, value in request.args.items() if key.startswith('sort_by')}

    filters = request.args.get('filters', default='{}', type=str)
    filters_dict = json.loads(filters)
#
    delivery_service.filter(filters=filters_dict)
    
    if sort_params:
        # Применяем сортировку, а затем пагинацию
        delivery_service.sort(**sort_params)
        # Пагинация вручную для отфильтрованных данных
        start = (page - 1) * size
        end = start + size
        deliveries = delivery_service.get_with_pagination(page, size)
    else:
        # Применяем только пагинацию
        deliveries = delivery_service.get_with_pagination(page, size)

    serializer = UniversalSerializer(DBSDelivery, many = True)
    deliveries_data = serializer.dump(deliveries)

    json_data = {
        'page': page,
        'size': size,
        'total': len(deliveries_data),
        'data': deliveries_data
    }

    return jsonify(json_data)