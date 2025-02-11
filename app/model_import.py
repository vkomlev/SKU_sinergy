# app/model_import.py

from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Sequence, Index, text
from sqlalchemy.ext.declarative import declarative_base
from app.model_registry import register_model

Base = declarative_base()

class DBSDelivery(Base):
    __tablename__ = 'DBS_delivery'
    __table_args__ = {'schema': 'import'}  # Указание схемы
    
    id_dbs = Column(Integer, server_default=text("nextval('import.\"DBS_delivery_id_dbs_seq\"'::regclass)"), primary_key=True)
    marketplace = Column(String)
    partner = Column(String)
    assembly_task = Column(String)
    sku = Column(String)
    product_name = Column(String)
    delivery_date_planned = Column(String)
    delivery_date_actual = Column(String)
    delivery_time = Column(String)
    delivery_address = Column(String)
    client_name = Column(String)
    climb = Column(String)
    status = Column(String)
    delivery_man = Column(String)
    distance = Column(String)
    cost = Column(Integer)
    payment_status = Column(String)
    compensation = Column(String)
    note = Column(String)
    delivery_date_actual_finished = Column(Date)
    delivery_date_plan_finished = Column(Date)


class OrdersOzon(Base):
    __tablename__ = 'orders_ozon'
    __table_args__ = (
        Index('orders_ozon_order_number_idx', 'order_number', 'ship_number', unique=True),
        {'schema': 'import'}  # Важно: это должно быть частью словаря
    )
    
    order_number = Column(String, nullable=False)
    ship_number = Column(String, nullable=False)
    date_accept = Column(DateTime)
    date_ship = Column(DateTime)
    status = Column(String)
    date_delivery = Column(DateTime)
    date_transfer = Column(DateTime)
    summ_ship = Column(Float)
    currency_ship = Column(String)
    product_name = Column(String)
    ozon_id = Column(Integer)
    sku = Column(String)
    final_cost = Column(Float)
    currency_product = Column(String)
    client_cost = Column(Float)
    client_currency = Column(String)
    product_count = Column(Integer)
    delivery_cost = Column(Float)
    linked_ships = Column(String)
    redeemed_product = Column(String)
    cost_before_discount = Column(Float)
    discount_percent = Column(String)
    discount_rub = Column(Float)
    actions = Column(String)
    climb = Column(String)
    upper_barcode = Column(String)
    lower_barcode = Column(String)
    shipping_cluster = Column(String)
    delivery_cluster = Column(String)
    delivery_region = Column(String)
    delivery_city = Column(String)
    delivery_type = Column(String)
    client_segment = Column(String)
    payment_type = Column(String)
    legal_entity = Column(String)
    client_name = Column(String)
    client_phone = Column(String)
    client_email = Column(String)
    recipient_name = Column(String)
    recipient_phone = Column(String)
    delivery_address = Column(String)
    postal_code = Column(String)
    shipping_warehouse = Column(String)
    carrier = Column(String)
    method_name = Column(String)
    weight = Column(Float)
    jewelry_barcode = Column(String)
    id_oo = Column(Integer, primary_key=True, server_default=text("nextval('import.orders_ozon_id_oo_seq'::regclass)"))

register_model(DBSDelivery)
register_model(OrdersOzon)