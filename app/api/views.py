from flask import request, jsonify
from app.services.base_service import BaseService
from app.utils.helpers import get_session
from app.repositories.base_repository import BaseRepository
from app.controllers.base_controller import BaseController
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
