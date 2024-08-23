# SKU_Project/settings.py

import os

# Конфиг подключения к БД
DATABASE = {
    'drivername': 'postgresql',
    'host': os.getenv('DB_HOST', '26.43.234.104'),
    'port': os.getenv('DB_PORT', '5432'),
    'username': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'MSC7558866'),
    'database': os.getenv('DB_NAME', 'SKU'),
}
