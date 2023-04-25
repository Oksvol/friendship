from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

yn_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Да"),
        KeyboardButton(text="Нет")
    ]
],
    resize_keyboard=True)
