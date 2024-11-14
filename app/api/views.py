from flask import request, jsonify
from app.services.base_service import BaseService
from app.utils.helpers import get_session
from app.utils.runners import run_r_script
from app.repositories.base_repository import BaseRepository
from app.controllers.base_controller import BaseController
from app.utils.road_distance import RoadDistance
import logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def upload_file():
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


def upload_to_table(table_name):
    # Реализация загрузки файла
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
    
def r_script():
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

def calculate_distance():
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

def mkad_distance():
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
