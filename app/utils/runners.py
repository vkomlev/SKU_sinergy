import subprocess
import os
import logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_r_script(path_to_r_script):
    try:
        # Получаем абсолютный путь к R скрипту
        script_path = os.path.abspath(path_to_r_script)
        
        # Устанавливаем рабочую папку равную папке скрипта
        script_dir = os.path.dirname(script_path)
        
        # Проверяем существование скрипта
        if not os.path.exists(script_path):
            return {"status": "fail", "message": "R script not found."}
        
        # Запускаем R скрипт с помощью subprocess
        result = subprocess.run(
            ["Rscript", "--no-save", "--no-restore", script_path],
            cwd=script_dir,
            capture_output=True,
            text=True,
            errors='ignore',  # Игнорировать недекодируемые символы
            encoding='utf-8'
        )
        return result
    except Exception as e:
        logger.error(f"Error executing R script: {e}")
        return {"status": "fail", "message": f"Error executing R script. Error: {e}"}