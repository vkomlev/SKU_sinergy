# app/main/urls.py

from .views import index_view, orders_view, delivery_view

def setup_routes(app):
    app.add_url_rule('/', 'index', index_view)
    app.add_url_rule('/orders', 'orders', orders_view)
    app.add_url_rule('/delivery', 'delivery', delivery_view)