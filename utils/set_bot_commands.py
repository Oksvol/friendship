from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("menu", "Меню бота"),
            types.BotCommand("lk", "Личный кабинет"),
            types.BotCommand("help", "Помощь")
        ]
    )