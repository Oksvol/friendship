from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#Документация по текстовым кнопкам: https://core.telegram.org/bots/api#replykeyboardmarkup

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Меню"),
        ],
        [
            KeyboardButton(text="Помощь"),
            KeyboardButton(text="Правила")
        ],
        [
            KeyboardButton(text="Связаться/подписаться"),
        ],
    ],
    resize_keyboard=True
)