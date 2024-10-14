#app/api/tables/views.py

import json
from flask import request, jsonify, abort

from app.utils.helpers import get_session
from app.utils.metadata import MetadataManager

from app.model_import import DBSDelivery
from app.api.tables.serializers import UniversalSerializer
from app.services.base_service import BaseService
from app.repositories.base_repository import BaseRepository
from app.controllers.base_controller import BaseController

def get_data_view(table_name):
    session = get_session()
    model = BaseRepository.get_model_by_table_name(table_name.replace('_', '.', 1))

    try:
            metadata_manager = MetadataManager()
            metadata_json = metadata_manager.get_metadata(table_name)
            view_name = metadata_json.get('view_name')
            if view_name:
                view_name = view_name.replace('_', '.', 1)
                model = BaseRepository.get_model_by_table_name(view_name)
    except Exception as e:
            print(f'Модель не найдена или не существует: {e}')
            pass  # If view metadata is not found, fallback to original table model

    service = BaseService(BaseController(BaseRepository(model, session)))
    
    page = request.args.get('page', default=1, type=int)
    size = request.args.get('size', default=25, type=int)

    sort_params = {key: value for key, value in request.args.items() if key.startswith('sort_by')}

    filters = request.args.get('filters', default='{}', type=str)
    filters_dict = json.loads(filters)

    service.filter(filters=filters_dict)
    
    if sort_params:
        # Apply sorting and then pagination
        service.sort(**sort_params)
        # Manual pagination for filtered data
        start = (page - 1) * size
        end = start + size
        deliveries = service.get_with_pagination(page, size)
    else:
        # Apply only pagination
        deliveries = service.get_with_pagination(page, size)

    serializer = UniversalSerializer(model, many=True)
    deliveries_data = serializer.dump(deliveries)

    json_data = {
        'page': page,
        'size': size,
        'total': service.get_count(),
        'data': deliveries_data
    }

    return jsonify(json_data)

def get_metadata_view(table_name):
    session = get_session()
    
    model = BaseRepository.get_model_by_table_name(table_name.replace('_', '.', 1))
    
    try:
            metadata_manager = MetadataManager()
            metadata_json = metadata_manager.get_metadata(table_name)
            view_name = metadata_json.get('view_name')
            if view_name:
                view_name = view_name.replace('_', '.', 1)
                model = BaseRepository.get_model_by_table_name(view_name)
    except Exception:
            pass  # If view metadata is not found, fallback to original table model

    service = BaseService(BaseController(BaseRepository(model, session)))
    metadata = service.get_table_metadata()
    return jsonify(metadata)

def search(table_name):
    session = get_session()    
    model = BaseRepository.get_model_by_table_name(table_name.replace('_', '.', 1))

    try:
            metadata_manager = MetadataManager()
            metadata_json = metadata_manager.get_metadata(table_name)
            view_name = metadata_json.get('view_name')
            if view_name:
                model = BaseRepository.get_model_by_table_name(view_name)
    except Exception:
            pass  # If view metadata is not found, fallback to original table model
    service = BaseService(BaseController(BaseRepository(model, session)))
    query = request.args.get('query', default = '', type= str)

    results = service.search(query)
    total = len(results) #подсчет записей

    serialized_results = UniversalSerializer(model, many=True).dump(results) # Сереализатор для преобразования результатов в JSON
    query_results = {"total":total, 
                     "data": serialized_results}
    return jsonify(query_results)

def create_record(table_name):
    session = get_session()
    model = BaseRepository.get_model_by_table_name(table_name.replace('_', '.', 1))
    service = BaseService(BaseController(BaseRepository(model, session)))
    data = request.get_json()
    #short_table_name = table_name.replace(table_name[:table_name.find('_')+1],'')
    short_table_name = table_name.replace('_', '.', 1)
    new_record = service.create_data(data, short_table_name)
    if new_record:
        return jsonify(UniversalSerializer(model).dump(new_record)), 201
    else:
        abort(404, description="Record not created")


def update_record(table_name, record_id):
    session = get_session()
    model = BaseRepository.get_model_by_table_name(table_name.replace('_', '.', 1))
    service = BaseService(BaseController(BaseRepository(model, session)))
    data = request.get_json()
    updated_record = service.update_data(record_id, data)
    if updated_record:
        return jsonify(UniversalSerializer(model).dump(updated_record)), 200
    else:
        abort(404, description="Record not found")


def delete_record(table_name, record_id):
    session = get_session()
    model = BaseRepository.get_model_by_table_name(table_name.replace('_', '.', 1))
    service = BaseService(BaseController(BaseRepository(model, session)))
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
    model = BaseRepository.get_model_by_table_name(table_name.replace('_', '.', 1))
    service = BaseService(BaseController(BaseRepository(model, session)))
    record = service.get_record(record_id)
    if record:
        return jsonify(UniversalSerializer(model).dump(record)), 200
    else:
        abort(404, description="Record not found")

