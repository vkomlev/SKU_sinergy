# app/api/views.py

"""
Модуль обработчиков API-запросов.

Этот модуль содержит обработчики API для работы с загрузкой файлов, выполнения R-скриптов, 
расчёта расстояний и загрузки данных маркетплейсов Ozon и Wildberries.

Функции:
- `upload_file() -> tuple[Response, int]`: Загружает произвольный файл на сервер.
- `upload_to_table(table_name: str) -> tuple[Response, int]`: Загружает файл в указанную таблицу базы данных.
- `r_script() -> tuple[Response, int]`: Выполняет R-скрипт по заданному пути.
- `calculate_distance() -> tuple[Response, int]`: Вычисляет расстояние между двумя адресами.
- `mkad_distance() -> tuple[Response, int]`: Рассчитывает расстояние от МКАД до указанного адреса.
- `ozon_dbs_api_load() -> tuple[Response, int]`: Загружает отправления Ozon DBS.
- `wb_dbs_api_load() -> tuple[Response, int]`: Загружает отправления Wildberries DBS.
"""

from flask import request, jsonify, Response

from app.services.base_service import BaseService
from app.utils.helpers import get_session
from app.utils.runners import run_r_script
from app.repositories.base_repository import BaseRepository
from app.controllers.base_controller import BaseController
from app.utils.road_distance import RoadDistance
from logging_config import logger

def upload_file() -> tuple[Response, int]:
    """
    Загружает файл на сервер.

    Returns:
        tuple[Response, int]: JSON-ответ с результатом загрузки.
    """

    if 'file' not in request.files:
        return jsonify({"status": "fail", "message": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"status": "fail", "message": "No selected file"}), 400

    file_id = BaseService.upload_file_to_server(file)
    if file_id:
        return jsonify({
                "status": "success",
                "file_id": file_id,
                "message": "File uploaded successfully."
            }), 200
    else:
        return jsonify({"status": "fail", "message": "File upload failed."}), 500


def upload_to_table(table_name: str) -> tuple[Response, int]:
    """
    Загружает файл в указанную таблицу базы данных.

    Args:
        table_name (str): Название таблицы.

    Returns:
        tuple[Response, int]: JSON-ответ с результатом загрузки данных.
    """

    try:
        logger.info (f'Начало загрузки')
        if 'file' not in request.files:
            return jsonify({"status": "fail", "message": "No file part in the request"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"status": "fail", "message": "No selected file"}), 400
        try:
            logger.info (f'{file.filename}')
            model = BaseRepository.get_model_by_table_name(table_name.replace('_', '.', 1))
            session = get_session()
            service = BaseService(BaseController(BaseRepository(model, session)))
            fail = service.load_transormed_data(file)
            if not fail:
                return jsonify({
                        "status": "success",
                        "message": "Данные загружены в БД."
                    }), 200
            else:
                return jsonify(fail[0]), fail[1]
            logger.info (f'Окончание загрузки')
        except Exception as e:
            return jsonify({"status": "fail", "message": f"File upload failed. Error: {e}"}), 500
    except Exception as e:
        logger.error (f'Ошибка: {e}')
        return jsonify({"status": "fail", "message": f"File upload failed. Error: {e}"}), 500
    
def r_script() -> tuple[Response, int]:
    """
    Выполняет R-скрипт по заданному пути.

    Returns:
        tuple[Response, int]: JSON-ответ с результатами выполнения R-скрипта.
    """

    path = request.args.get('path')
    if not path:
        return jsonify({"status": "fail", "message": "Path not provided"}), 400
    result = run_r_script(path)
    if isinstance(result, dict):
        if result.get('status') == 'fail' and result.get('message') =='R script not found.':
            return jsonify({"status": "fail", "message": "R script not found."}), 404
        elif result.get('status') == 'fail':
             return jsonify({"status": "fail", "message": result.get('message')}), 500
    else:
        if result.returncode != 0:
            logger.error(f"R script failed: {result.stderr}")
            return jsonify({"status": "fail", "message": f"R script execution failed. Error: {result.stderr}"}), 500
    logger.info(f"R script executed successfully: {result.stdout}")
    return jsonify({"status": "success", "message": "R script executed successfully.", "output": result.stdout}), 200

def calculate_distance() -> tuple[Response, int]:
    """
    Рассчитывает расстояние между двумя адресами.

    Returns:
        tuple[Response, int]: JSON-ответ с вычисленным расстоянием.
    """

    try:
        locations = request.args.get("locations")
        api_key = request.args.get("api_key")

        if not locations:
            return jsonify({"error": "Отсутствует обязательный параметр: 'locations'"}), 400
        if api_key:
            distance = RoadDistance(api_key=api_key)            
        else:
            distance = RoadDistance()
        return jsonify(distance.get_distance(locations))
    except Exception as e:
        logger.error(f"Ошибка при расчете расстояния: {e}")
        return jsonify({"error": str(e)}), 500

def mkad_distance() -> tuple[Response, int]:
    """
    Рассчитывает расстояние от МКАД до указанного адреса.

    Returns:
        tuple[Response, int]: JSON-ответ с рассчитанным расстоянием.
    """

    try:
        location = request.args.get("location")
        api_key = request.args.get("api_key")
        max_points = request.args.get("max_points", 3)
        if not location:
            return jsonify({"error": "Отсутствует обязательный параметр: 'location'"}), 400
        if api_key:
            distance = RoadDistance(api_key=api_key)            
        else:
            distance = RoadDistance()
        return jsonify(distance.get_mkad_distance(location, max_points))
    except Exception as e:
        logger.error(f"Ошибка при расчете расстояния от МКАД: {e}")
        return jsonify({"error": str(e)}), 500

def ozon_dbs_api_load() -> tuple[Response, int]:
    """
    Загружает данные отправлений Ozon DBS.

    Returns:
        tuple[Response, int]: JSON-ответ с результатами загрузки.
    """

    try:
        model = BaseRepository.get_model_by_table_name('main.delivery')
        session = get_session()
        service = BaseService(BaseController(BaseRepository(model, session)))
        result = jsonify(service.extract_ozon_dbs()), 200
        logger.info(f"Ozon DBS loaded successfully")
        return result 
    except Exception as e:
        logger.error(f"Ошибка при загрузке Ozon DBS: {e}")
        return jsonify({"error": str(e)}), 500

def wb_dbs_api_load() -> tuple[Response, int]:
    """
    Загружает данные отправлений Wildberries DBS.

    Returns:
        tuple[Response, int]: JSON-ответ с результатами загрузки.
    """

    try:
        model = BaseRepository.get_model_by_table_name('main.delivery')
        session = get_session()
        service = BaseService(BaseController(BaseRepository(model, session)))
        result = jsonify(service.extract_wb_dbs()), 200
        logger.info(f"WB DBS loaded successfully")
        return result
    except Exception as e:
        logger.error(f"Ошибка при загрузке WB DBS: {e}")
        return jsonify({"error": str(e)}), 500