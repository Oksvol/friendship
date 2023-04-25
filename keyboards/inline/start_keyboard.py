from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_keyboard = InlineKeyboardMarkup(row_width=2,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(text="Отправить посылку", callback_data='sending'),
                                              InlineKeyboardButton(text="Рассказать о поездке",
                                                                   callback_data='delivery')
                                          ],
                                          [
                                              InlineKeyboardButton(text="Отмена", callback_data="next")
                                          ]
                                      ])
