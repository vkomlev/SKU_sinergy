#app/api/tables/views.py

import json
from flask import request, jsonify, abort

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
        'total': delivery_service.get_count(),
        'data': deliveries_data
    }

    return jsonify(json_data)

def get_metadata_view():
    session = get_session()
    service = ImportDBSDeliveryService(session)
    metadata = service.get_table_metadata()
    return jsonify(metadata)

def search():
    session = get_session()
    service = ImportDBSDeliveryService(session)
    query = request.args.get('query', default = '', type= str)

    results = service.search(query)
    total = len(results) #подсчет записей

    serialized_results = UniversalSerializer(DBSDelivery, many=True).dump(results) # Сереализатор для преобразования результатов в JSON
    query_results = {"total":total, 
                     "data": serialized_results}
    return jsonify(query_results)

def create_record(table_name):
    session = get_session()
    service = ImportDBSDeliveryService(session)
    data = request.get_json()
    #short_table_name = table_name.replace(table_name[:table_name.find('_')+1],'')
    short_table_name = table_name.replace('_', '.', 1)
    new_record = service.create_data(data, short_table_name)
    if new_record:
        return jsonify(UniversalSerializer(DBSDelivery).dump(new_record)), 201
    else:
        abort(404, description="Record not created")


def update_record(table_name, record_id):
    session = get_session()
    service = ImportDBSDeliveryService(session)
    data = request.get_json()
    updated_record = service.update_data(record_id, data)
    if updated_record:
        return jsonify(UniversalSerializer(DBSDelivery).dump(updated_record)), 200
    else:
        abort(404, description="Record not found")


def delete_record(table_name, record_id):
    session = get_session()
    service = ImportDBSDeliveryService(session)
    result = service.delete_data(record_id)
    if result:
        return jsonify({
            "status": "success",
            "message": "Record deleted successfully."
            }), 200
    else:
        abort(404, description="Record not found")

def get_record(table_name, record_id):
    session = get_session()
    service = ImportDBSDeliveryService(session)
    record = service.get_record(record_id)
    if record:
        return jsonify(UniversalSerializer(DBSDelivery).dump(record)), 200
    else:
        abort(404, description="Record not found")

