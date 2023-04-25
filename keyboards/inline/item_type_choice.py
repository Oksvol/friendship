from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def create_item_type_choice_keyboard(btns: dict):
    item_type_choice_keyboard = InlineKeyboardMarkup(row_width=2)

    for cdata, text in btns.items():
        button = InlineKeyboardButton(
                text=f"{text}",
                callback_data=f"{cdata}"
            )

        item_type_choice_keyboard.add(button)

    return item_type_choice_keyboard, btns