# ./wsgi.py

"""Модуль запуска WSGI-сервера для приложения SKU_sinergy.

Предназначен для определения точки входа WSGI-сервера.
"""

from app.main import create_app

# Создание экземпляра приложения
application = create_app()

if __name__ == "__main__":
    # Запуск приложения для отладки
    application.run(host="0.0.0.0", port=5000, debug=True)
