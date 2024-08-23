# app/main/views.py

from flask import render_template, request
from app.utils.helpers import get_session
from app.services.import_ozon_orders_service import ImportOzonOrdersService
from app.services.import_DBS_delivery_service import ImportDBSDeliveryService

def index_view():
    return render_template('index.html')

def orders_view():
    session = get_session()
    orders_service = ImportOzonOrdersService(session)
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    orders = orders_service.get_with_pagination(page, per_page)
    return render_template('orders.html', orders=orders, page=page)

def delivery_view():
    session = get_session()
    delivery_service = ImportDBSDeliveryService(session)
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    deliveries = delivery_service.get_with_pagination(page, per_page)
    return render_template('delivery.html', deliveries=deliveries, page=page)
