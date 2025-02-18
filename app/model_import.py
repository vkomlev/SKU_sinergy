# app/model_import.py

"""
Модуль описывает модели таблиц базы данных, используемые для хранения информации о доставках DBS 
и заказах Ozon. Реализован с использованием SQLAlchemy.

- `DBSDelivery`: таблица `DBS_delivery` в схеме `import`, содержащая данные о доставках.
- `OrdersOzon`: таблица `orders_ozon` в схеме `import`, содержащая данные о заказах Ozon.

Обе модели регистрируются с помощью функции `register_model`, что позволяет управлять их доступностью в системе.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Sequence, Index, text
from sqlalchemy.ext.declarative import declarative_base
from app.model_registry import register_model

# Базовый класс моделей SQLAlchemy
Base = declarative_base()


class DBSDelivery(Base):
    """
    Модель таблицы `DBS_delivery`, содержащей информацию о доставках DBS.

    Атрибуты:
        id_dbs (int): Уникальный идентификатор доставки.
        marketplace (str): Название маркетплейса.
        partner (str): Партнёрская организация.
        assembly_task (str): Код сборочного задания.
        sku (str): Идентификатор товара.
        product_name (str): Название товара.
        delivery_date_planned (str): Планируемая дата доставки.
        delivery_date_actual (str): Фактическая дата доставки.
        delivery_time (str): Время доставки.
        delivery_address (str): Адрес доставки.
        client_name (str): Имя клиента.
        climb (str): Подъём товара (например, на этаж).
        status (str): Статус доставки.
        delivery_man (str): Информация о курьере.
        distance (str): Расстояние доставки.
        cost (int): Стоимость доставки.
        payment_status (str): Статус оплаты.
        compensation (str): Компенсация при проблемах с доставкой.
        note (str): Дополнительные заметки.
        delivery_date_actual_finished (Date): Дата фактического завершения доставки.
        delivery_date_plan_finished (Date): Дата планируемого завершения доставки.
    """

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
    """
    Модель таблицы `orders_ozon`, содержащей информацию о заказах Ozon.

    Атрибуты:
        order_number (str): Номер заказа.
        ship_number (str): Номер отгрузки.
        date_accept (datetime): Дата приёма заказа.
        date_ship (datetime): Дата отгрузки.
        status (str): Статус заказа.
        date_delivery (datetime): Дата доставки.
        date_transfer (datetime): Дата передачи заказа.
        summ_ship (float): Сумма заказа.
        currency_ship (str): Валюта заказа.
        product_name (str): Название товара.
        ozon_id (int): Идентификатор товара на Ozon.
        sku (str): SKU товара.
        final_cost (float): Итоговая стоимость товара.
        currency_product (str): Валюта товара.
        client_cost (float): Цена товара для клиента.
        client_currency (str): Валюта клиента.
        product_count (int): Количество товаров в заказе.
        delivery_cost (float): Стоимость доставки.
        linked_ships (str): Связанные отгрузки.
        redeemed_product (str): Информация о выкупе товара.
        cost_before_discount (float): Стоимость до скидки.
        discount_percent (str): Процент скидки.
        discount_rub (float): Сумма скидки в рублях.
        actions (str): Акции, применённые к заказу.
        climb (str): Доставка с подъёмом.
        upper_barcode (str): Верхний штрихкод.
        lower_barcode (str): Нижний штрихкод.
        shipping_cluster (str): Кластер доставки.
        delivery_cluster (str): Кластер получения.
        delivery_region (str): Регион доставки.
        delivery_city (str): Город доставки.
        delivery_type (str): Тип доставки.
        client_segment (str): Сегмент клиента.
        payment_type (str): Тип оплаты.
        legal_entity (str): Юридическое лицо.
        client_name (str): Имя клиента.
        client_phone (str): Телефон клиента.
        client_email (str): Email клиента.
        recipient_name (str): Имя получателя.
        recipient_phone (str): Телефон получателя.
        delivery_address (str): Адрес доставки.
        postal_code (str): Почтовый индекс.
        shipping_warehouse (str): Склад отправки.
        carrier (str): Перевозчик.
        method_name (str): Метод доставки.
        weight (float): Вес товара.
        jewelry_barcode (str): Штрихкод для ювелирных изделий.
        id_oo (int): Уникальный идентификатор заказа в базе.
    """

    __tablename__ = 'orders_ozon'
    __table_args__ = (
        Index('orders_ozon_order_number_idx', 'order_number', 'ship_number', unique=True),
        {'schema': 'import'}  # Указание схемы
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

# Регистрация моделей в системе
register_model(DBSDelivery)
register_model(OrdersOzon)
