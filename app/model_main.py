# coding: utf-8
from sqlalchemy import ARRAY, Column, Date, DateTime, Float, ForeignKey, Index, Integer, SmallInteger, String, Text, text, Table
from sqlalchemy.dialects.postgresql import JSONB, MONEY
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.model_registry import register_model

Base = declarative_base()
metadata = Base.metadata


class Brands(Base):
    __tablename__ = 'brands'
    __table_args__ = {'schema': 'main', 'comment': 'Производители (бренды)'}

    id_brand = Column(Integer, primary_key=True, server_default=text("nextval('main.brands_id_brand_seq'::regclass)"))
    brand_name = Column(String, nullable=False)


class DeliveryCompany(Base):
    __tablename__ = 'delivery_company'
    __table_args__ = {'schema': 'main'}

    id_dc = Column(SmallInteger, primary_key=True, server_default=text("nextval('main.delivery_company_id_dc_seq'::regclass)"))
    dc_name = Column(String)


class DeliveryStatus(Base):
    __tablename__ = 'delivery_status'
    __table_args__ = {'schema': 'main', 'comment': 'Статусы доставки'}

    ds_name = Column(String)
    id_ds = Column(SmallInteger, primary_key=True, server_default=text("nextval('main.delivery_status_id_ds_seq'::regclass)"))


class Incomes(Base):
    __tablename__ = 'incomes'
    __table_args__ = {'schema': 'main', 'comment': 'Начисления от маркетплейсов (расходы при работе с маркетплейсами)'}

    id_income = Column(Integer, primary_key=True, server_default=text("nextval('main.incomes_id_income_seq'::regclass)"))
    id_order = Column(Integer, comment='Код заказа')
    equiring = Column(MONEY, comment='Расходы на эквайринг')
    delivery_cost = Column(MONEY, comment='Расходы на доставку')


class Marketpalces(Base):
    __tablename__ = 'marketpalces'
    __table_args__ = {'schema': 'main', 'comment': 'Маркетплейсы'}

    id_marketplace = Column(SmallInteger, primary_key=True, server_default=text("nextval('main.marketpalces_id_marketplace_seq'::regclass)"))
    mp_name = Column(String, nullable=False, comment='Название площадки (маркетплейса)')
    create_time = Column(DateTime(True), server_default=text("now()"))
    update_time = Column(DateTime(True), server_default=text("now()"))
    pseudonyms = Column(ARRAY(String()))


class Obx(Base):
    __tablename__ = 'obx'
    __table_args__ = {'schema': 'main', 'comment': 'Объемно-весовые характеристики товаров'}

    id_obx = Column(Integer, primary_key=True, server_default=text("nextval('main.obx_id_obx_seq'::regclass)"))
    obx_type = Column(SmallInteger, comment='Тип: 0 - нетто, 1 - брутто')
    weight = Column(Float, comment='Масса в килограммах')
    length = Column(Integer, comment='Длина товара в сантиметрах')
    width = Column(Integer, comment='Ширина товара в сантиметрах')
    height = Column(Integer, comment='Высота товара в сантиметрах')
    id_product = Column(Integer, comment='Код товара')
    sku = Column(String, comment='Артикул товара')


class Orders(Base):
    __tablename__ = 'orders'
    __table_args__ = {'schema': 'main', 'comment': 'Заказы'}

    id_order = Column(Integer, primary_key=True, server_default=text("nextval('main.orders_id_order_seq'::regclass)"))
    order_number = Column(String, nullable=False, unique=True, comment='Номер заказа')
    id_markeplace = Column(SmallInteger)
    departure_number = Column(String, comment='Номер отправления')


class Partners(Base):
    __tablename__ = 'partners'
    __table_args__ = {'schema': 'main'}

    id_partner = Column(Integer, primary_key=True, server_default=text("nextval('main.partners_id_partner_seq'::regclass)"))
    partner_name = Column(String)
    pseudonyms = Column(ARRAY(String()))
    description = Column(String)


class ProductCategory(Base):
    __tablename__ = 'product_category'
    __table_args__ = {'schema': 'main', 'comment': 'Категории товаров'}

    id_pc = Column(SmallInteger, primary_key=True, server_default=text("nextval('main.product_category_id_pc_seq'::regclass)"))
    pc_name = Column(String, nullable=False, comment='Название катагории')
    create_time = Column(DateTime(True), server_default=text("now()"), comment='Дата создания')
    status = Column(SmallInteger, server_default=text("1"), comment='Статус')
    enabled_char = Column(JSONB(astext_type=Text()), comment='Характеристики, которые доступны для редактирования для выбранной группы')


class MarketplaceCategoryMapping(Base):
    __tablename__ = 'marketplace_category_mapping'
    __table_args__ = {'schema': 'main', 'comment': 'Маппинг категорий товаров для конкретного макретплейса'}

    id_mcm = Column(Integer, primary_key=True, server_default=text("nextval('main.marketplace_category_mapping_id_mcm_seq'::regclass)"))
    id_pc = Column(ForeignKey('main.product_category.id_pc', ondelete='CASCADE'), comment='Внутренний код категории товара')
    id_marketplace = Column(ForeignKey('main.marketpalces.id_marketplace', ondelete='CASCADE'), comment='Маркетплейс')
    category_name = Column(String, nullable=False, comment='Название категории на площадке маркетплейса')

    marketpalce = relationship('Marketpalces')
    product_category = relationship('ProductCategory')


class Products(Base):
    __tablename__ = 'products'
    __table_args__ = {'schema': 'main', 'comment': 'Товары'}

    id_product = Column(Integer, primary_key=True, server_default=text("nextval('main.products_id_product_seq'::regclass)"))
    product_name = Column(String, comment='Название товара')
    sku = Column(String, nullable=False, unique=True, comment='Артикул')
    id_pc = Column(ForeignKey('main.product_category.id_pc', ondelete='RESTRICT'), nullable=False, comment='Категория')
    characteristics = Column(JSONB(astext_type=Text()), comment='Характеристики товара')
    description_default = Column(Text, comment='Описание по умолчанию')
    create_time = Column(DateTime(True), server_default=text("now()"), comment='Дата заведения')
    update_time = Column(DateTime(True), server_default=text("now()"), comment='Дата последней редакции')
    who_update = Column(Integer, comment='Кто обновил')
    id_brand = Column(ForeignKey('main.brands.id_brand', ondelete='RESTRICT'), comment='Бренд')

    brand = relationship('Brands')
    product_category = relationship('ProductCategory')


class CostHistory(Base):
    __tablename__ = 'cost_history'
    __table_args__ = {'schema': 'main', 'comment': 'История себестоимости'}

    id_ch = Column(Integer, primary_key=True, server_default=text("nextval('main.cost_history_id_ch_seq'::regclass)"))
    id_product = Column(ForeignKey('main.products.id_product'), nullable=False, comment='Товар')
    cost_value = Column(MONEY, comment='Значение цены')
    update_date = Column(Date, server_default=text("(now())::date"), comment='Дата изменения')

    product = relationship('Products')


class Delivery(Base):
    __tablename__ = 'delivery'
    __table_args__ = {'schema': 'main', 'comment': 'Информация о доставках'}

    id_delivery = Column(Integer, primary_key=True, server_default=text("nextval('main.delivery_id_delivery_seq'::regclass)"))
    id_marketplace = Column(ForeignKey('main.marketpalces.id_marketplace', ondelete='RESTRICT'))
    id_partner = Column(ForeignKey('main.partners.id_partner', ondelete='RESTRICT'))
    assembly_task = Column(String)
    id_product = Column(ForeignKey('main.products.id_product', ondelete='RESTRICT'), nullable=False)
    delivery_date_planned = Column(Date)
    delivery_date_actual = Column(Date)
    delivery_time = Column(String)
    delivery_address = Column(String)
    client_name = Column(String)
    climb = Column(String)
    id_ds = Column(ForeignKey('main.delivery_status.id_ds', ondelete='RESTRICT'))
    distance = Column(Float)
    id_dc = Column(ForeignKey('main.delivery_company.id_dc', ondelete='RESTRICT'), comment='Доставщик')
    cost = Column(MONEY)
    payment_status = Column(String)
    compensation = Column(String)
    note = Column(Text)

    delivery_company = relationship('DeliveryCompany')
    delivery_statu = relationship('DeliveryStatus')
    marketpalce = relationship('Marketpalces')
    partner = relationship('Partners')
    product = relationship('Products')


class Marginality(Base):
    __tablename__ = 'marginality'
    __table_args__ = {'schema': 'main', 'comment': 'Маржинальность цены на товар'}

    id_marginality = Column(Integer, primary_key=True, server_default=text("nextval('main.marginality_id_marginality_seq'::regclass)"))
    id_product = Column(ForeignKey('main.products.id_product', ondelete='CASCADE'))
    id_brand = Column(ForeignKey('main.brands.id_brand', ondelete='CASCADE'))
    margin_percent = Column(Float, comment='Ставка маржи')
    marginality = Column(MONEY, comment='Сумма маржи')

    brand = relationship('Brands')
    product = relationship('Products')


class Prices(Base):
    __tablename__ = 'prices'
    __table_args__ = {'schema': 'main', 'comment': 'Цены'}

    id_price = Column(Integer, primary_key=True, server_default=text("nextval('main.prices_id_price_seq'::regclass)"))
    id_marketplace = Column(ForeignKey('main.marketpalces.id_marketplace', ondelete='RESTRICT'))
    id_product = Column(ForeignKey('main.products.id_product', ondelete='RESTRICT'))
    price_fbs = Column(MONEY)
    price_fbo = Column(MONEY)
    price_dbs = Column(MONEY)
    price_mrc = Column(MONEY)

    marketpalce = relationship('Marketpalces')
    product = relationship('Products')


class ProductDescription(Base):
    __tablename__ = 'product_description'
    __table_args__ = (
        Index('product_description_id_product_idx', 'id_product', 'id_marketplace', unique=True),
        {'schema': 'main', 'comment': 'Описания товаров для различных площадок'}
    )

    id_pd = Column(Integer, primary_key=True, server_default=text("nextval('main.product_description_id_pd_seq'::regclass)"))
    description = Column(Text, nullable=False, comment='Описание')
    id_product = Column(ForeignKey('main.products.id_product', ondelete='CASCADE'), nullable=False, comment='Товар')
    id_marketplace = Column(ForeignKey('main.marketpalces.id_marketplace', ondelete='CASCADE'), comment='Маркетплейс')

    marketpalce = relationship('Marketpalces')
    product = relationship('Products')


class ProductMedia(Base):
    __tablename__ = 'product_media'
    __table_args__ = {'schema': 'main', 'comment': 'Фото и видео'}

    id_pm = Column(Integer, primary_key=True, server_default=text("nextval('main.product_media_id_pm_seq'::regclass)"))
    url = Column(String, nullable=False, comment='Ссылка на медиафайл')
    id_product = Column(ForeignKey('main.products.id_product', ondelete='CASCADE'), nullable=False)
    num = Column(SmallInteger, comment='Порядковый номер фото')

    product = relationship('Products')

t_vw_delivery = Table(
    'vw_delivery', metadata,
    Column('id_delivery', Integer),
    Column('mp_name', String),
    Column('partner_name', String),
    Column('assembly_task', String),
    Column('product_name', String),
    Column('delivery_date_planned', Date),
    Column('delivery_date_actual', Date),
    Column('delivery_time', String),
    Column('delivery_address', String),
    Column('client_name', String),
    Column('climb', String),
    Column('ds_name', String),
    Column('distance', Float),
    Column('dc_name', String),
    Column('cost', MONEY),
    Column('payment_status', String),
    Column('compensation', String),
    Column('note', Text),
    schema='main'
)


register_model(Brands)
register_model(DeliveryCompany)
register_model(DeliveryStatus)
register_model(Marketpalces)
register_model(Partners)
register_model(Products)
register_model(ProductDescription)
register_model(ProductMedia)
register_model(Prices)
register_model(Marginality)
register_model(Delivery)
register_model(MarketplaceCategoryMapping)
register_model(Incomes)
register_model(Obx)
register_model(Orders)
register_model(ProductCategory)
register_model(CostHistory)
register_model(t_vw_delivery)
