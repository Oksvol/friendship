from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

sending_items_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Документы/ключи/бумаги"),
        ],
        [
            KeyboardButton(text="Личные вещи")
        ],
        [
            KeyboardButton(text="Другое")
        ]
    ],
    resize_keyboard=True
)


role_choice = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отправлять"),
        ],
        [
            KeyboardButton(text="Получить")
        ]
    ],
    resize_keyboard=True
)
