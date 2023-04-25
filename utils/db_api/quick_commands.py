from datetime import date, datetime
from typing import List

from asyncpg import UniqueViolationError
from sqlalchemy import and_

from utils.db_api.db_gino import db
from utils.db_api.schemas.user import User
from utils.db_api.schemas.sending import Sending
from utils.db_api.schemas.delivery import Delivery


# Пользователи
async def add_user(id: int, full_name: str, username: str = None, contacts: str = None,
                   rating: float = None, sendings: str = None, deliveries: str = None, tokens: int = None):
    try:
        user = User(id=id, full_name=full_name, username=username, tokens=tokens)
        await user.create()

    except UniqueViolationError:
        pass


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def select_user(id: int):
    user = await User.query.where(User.id == id).gino.first()
    return user


async def count_users():
    total = await db.func.count(User.id).gino.scalar()
    return total


async def update_user_username(id, username):
    user = await User.get(id)
    await user.update(username=username).apply()


async def update_user_balance(id, balance):
    user = await User.get(id)
    await user.update(username=balance).apply()


# Отправления
async def add_sending(user_id: int, full_name: str,
                      send_from: str, send_to: str, delivery_date: date,
                      receiver_fio: str, item_type: str, payed: float = None, contacts: str = None,
                      username: str = None):

    sending = Sending(user_id=user_id, full_name=full_name, username=username, contacts=contacts,
                      send_from=send_from, send_to=send_to, delivery_date=delivery_date, receiver_fio=receiver_fio,
                      item_type=item_type)
    await sending.create()


'''
#Отправления
async def select_all_industries():
    industries = await Industry.query.gino.all()
    return industries

# async def get_industries() -> List[Share]:
#     return await Share.query.distinct(Share.industry_id).gino.all()


async def get_industries() -> List[Share]:

    return await Industry.query.distinct(Industry.code).gino.all()


async def select_industry(id: str):
    industry = await Industry.query.where(Industry.code == id).gino.first()
    return industry


#Акции
async def select_all_shares():
    shares = await Share.query.gino.all()
    return shares


async def get_shares(industry) -> List[Share]:
    shares = await Share.query.where(
        Share.industry_id == industry
    ).gino.all()
    return shares


async def get_share(tiker) -> Share:
    share = await Share.query.where(Share.tiker == tiker).gino.first()
    return share


async def update_share_quantity(tiker, quantity):
    share = await get_share(tiker)
    new_quantity = share.quantity + quantity
    await share.update(quantity=new_quantity).apply()


async def update_share_price(tiker, price):
    share = await get_share(tiker)
    await share.update(price=price).apply()



#Операции
async def select_all_operations():
    operations = await Operation.query.gino.all()
    return operations


async def add_operation(user_id: str, tiker: str, type: str, quantity: int, industry_id: str, price: float):
    operation = Operation(user_id=user_id, tiker=tiker, type=type, quantity=quantity, industry_id=industry_id, price=price)
    await operation.create()


async def get_operations_of_user_by_tiker(id: str, tiker: str) -> List[Operation]:
    user_operations = await Operation.query.where(and_(Operation.user_id == str(id),
                                                       Operation.tiker == tiker)).gino.all()

    return user_operations


async def get_operations_of_user(id: str) -> List[Operation]:
    user_operations = await Operation.query.where(Operation.user_id == str(id)).gino.all()

    return user_operations



#Глобальные новости
async def select_all_news_global():
    news_global = await News_Global.query.gino.all()
    return news_global


async def select_news_global_by_date(dt):
    news_global_from_date = await News_Global.query.where((News_Global.public_date == dt)).gino.all()
    return news_global_from_date

#Новости биржи
async def select_all_news_exchange():
    news_exchange = await News_Exchange.query.gino.all()
    return news_exchange


async def select_news_exchange_by_date(dt):
    news_exchange_from_date = await News_Exchange.query.where((News_Exchange.public_date == dt)).gino.all()
    return news_exchange_from_date

'''
