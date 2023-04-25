from sqlalchemy import Text, Column, BigInteger, String, sql, Numeric, Date

from utils.db_api.db_gino import TimedBaseModel


class Sending(TimedBaseModel):
    __tablename__ = 'sendings'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    full_name = Column(String(100))
    username = Column(Text)
    contacts = Column(Text, default=None)
    send_from = Column(Text)
    send_to = Column(Text)
    delivery_date = Column(Date)
    receiver_fio = Column(Text)
    item_type = Column(Text)
    payed = Column(Numeric(6, 2), default=0.00)

    query: sql.Select
