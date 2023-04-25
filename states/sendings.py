from aiogram.dispatcher.filters.state import StatesGroup, State


class Sending(StatesGroup):
    user_id = State()
    start_city = State()
    start_country = State()
    end_point = State()
    end_country = State()
    item_type = State()
    date_receiving = State()
    fio = State()
    role = State()
    receiver_fio = State()


