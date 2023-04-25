from sqlalchemy import Column, BigInteger, String, sql, Numeric, DateTime, SmallInteger, Text, Boolean

from utils.db_api.db_gino import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    full_name = Column(String(100))
    username = Column(String(100))
    contacts = Column(Text, default=None)
    sender_rating = Column(Numeric(1, 2), default=0.00)
    delivery_rating = Column(Numeric(1, 2), default=0.00)
    balance = Column(Numeric(6, 2), default=0.00)
    all_time_profit = Column(Numeric(6, 2), default=0.00)
    sendings = Column(Text, default=None)
    deliveries = Column(Text, default=None)
    active_deliveries = Column(Text, default=None)
    verification = Column(Boolean, default=False)
    passport = Column(String(120))
    tokens = Column(SmallInteger)

    query: sql.Select
