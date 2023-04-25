from aiogram.dispatcher.filters.state import StatesGroup, State


class Delivery(StatesGroup):
    user_id = State()
    start_city = State()
    start_country = State()
    end_point = State()
    end_country = State()
    between_points = State()
    transport = State()
    item_type = State()
    date_start = State()
    date_between = State()
    date_end = State()
    small_item = State()
    small_item_price = State()
    middle_item = State()
    middle_item_price = State()
    big_item = State()
    big_item_price = State()
    huge_item = State()
    huge_item_price = State()
    extra_item = State()
    extra_item_price = State()
    fio = State()
    contacts = State()