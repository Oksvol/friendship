from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, message
from aiogram.utils.callback_data import CallbackData

from loader import dp
from utils.db_api.quick_commands import get_industries, get_shares, get_operations_of_user_by_tiker

exchange_menu = CallbackData('exch', 'type')


def make_exchange_callback_data(type):
    return exchange_menu.new(type=type)


async def exchange_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)

    markup.insert(
        InlineKeyboardButton(
            text="Акции",
            callback_data="акции")
    )
    markup.insert(
        InlineKeyboardButton(
            text="Облигации",
            callback_data="облигации")
    )

    markup.row(
        InlineKeyboardButton(
            text="Назад в меню",
            callback_data="Меню")
    )

    return markup

