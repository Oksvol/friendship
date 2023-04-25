from aiogram import executor

from loader import dp, db, scheduler
from utils.db_api import db_gino
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Создает таблицы и подключение к бд
    print("Подключаем БД")
    await db_gino.on_startup(dp)
    print("Готово")

    print("Создаем таблицы")
    await db.gino.create_all()

    print("Готово")
    # Уведомляет про запуск
    await on_startup_notify(dp)
    # Устанавливаем дефолтные команды
    await set_default_commands(dp)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
