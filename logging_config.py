# ./logging_config.py

"""
Модуль конфигурирует систему логирования для приложения.

- Создаёт директорию `logs`, если она не существует.
- Настраивает логирование в файл `logs/app.log` с ротацией:
  - Максимальный размер файла: 10 MB.
  - Количество резервных файлов: 5.
  - Кодировка: UTF-8.
- Определяет формат логов и уровень логирования.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Создание директории для логов, если она не существует
log_directory: Path = Path('logs')
log_directory.mkdir(exist_ok=True)

# Настройка ротации логов
handler = RotatingFileHandler(
    log_directory / 'app.log',  # Файл для записи логов
    maxBytes = 10 * 1024 * 1024,  # Максимальный размер файла: 10 MB
    backupCount = 5,  # Количество резервных файлов
    encoding = 'utf-8'
)

# Конфигурация логирования
logging.basicConfig(
    handlers = [handler],
    level = logging.INFO,  # Уровень логирования: INFO
    format = '%(asctime)s - %(levelname)s - %(message)s',  # Формат логов
    datefmt = '%d.%m.%Y %H:%M:%S',  # Формат даты и времени
)

# Глобальный объект логгера
logger = logging.getLogger(__name__)
