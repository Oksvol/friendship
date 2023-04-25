from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


yn_keyboard = InlineKeyboardMarkup(row_width=2,
                                   inline_keyboard=[
                                       [
                                          InlineKeyboardButton(text="Да", callback_data='Yes'),
                                          InlineKeyboardButton(text="Нет",
                                                               callback_data='No')
                                       ]
                                   ])
