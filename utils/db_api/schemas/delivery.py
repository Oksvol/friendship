from sqlalchemy import Text, Column, BigInteger, String, sql, Numeric, Date

from utils.db_api.db_gino import TimedBaseModel


class Delivery(TimedBaseModel):
    __tablename__ = 'deliveries'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    full_name = Column(String(100))
    username = Column(Text)
    contacts = Column(Text)
    delivery_from = Column(Text)
    delivery_to = Column(Text)
    delivery_between_points = Column(Text)
    delivery_date_start = Column(Date)
    delivery_date_end = Column(Date)
    transport = Column(String(100))
    small_item = Column(Text)
    small_item_price = Column(Numeric(6, 2))
    middle_item = Column(Text)
    middle_item_price = Column(Numeric(6, 2))
    big_item = Column(Text)
    big_item_price = Column(Numeric(6, 2))
    huge_item = Column(Text)
    huge_item_price = Column(Numeric(6, 2))
    extra_item = Column(Text)
    extra_item_price = Column(Numeric(6, 2))
    ticket = Column(String(120))
    comment = Column(Text, default=None)

    query: sql.Select
