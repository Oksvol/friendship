from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.inline.start_keyboard import start_keyboard
from loader import dp
from utils.db_api import quick_commands as db

from utils.misc import rate_limit


@rate_limit(5, key="start")
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, ):
    await db.add_user(id=message.from_user.id,
                      full_name=message.from_user.full_name,
                      username=message.from_user.username,
                      tokens=1)

    await message.answer("Привет! Я FriendShip  бот.\n\n"
                         "С моей помощью вы можете отправить посылку в другую страну или город.\n\n"
                         "Или рассказать о своей поездке и возможности перевезти посылку в другую страну и заработать на этом.\n\n"
                         "С какой целью ты здесь?", reply_markup=start_keyboard
                         )
