from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, message
from aiogram.utils.callback_data import CallbackData

from loader import dp
from utils.db_api.quick_commands import get_industries, get_shares, get_operations_of_user_by_tiker
from utils.misc.count_share_balance import count_operations_by_tiker

menu_cd = CallbackData('show_menu', 'level', 'industry', 'tiker', 'user', 'type')
do_operation = CallbackData('deal', 'type', 'industry', 'tiker', 'user')



def make_callback_data(level, industry='0', tiker='0', user=0, type=0):
    return menu_cd.new(level=level,
                       industry=industry, tiker=tiker, user=int(user), type=type)



async def industries_keyboard(user):
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=1)

    industries = await get_industries()

    for industry in industries:
        button_text = f'{industry.title}'
        callback_data = make_callback_data(level=CURRENT_LEVEL+1,
                                           industry=industry.code,
                                           user=user
                                           )

        markup.insert(
            InlineKeyboardButton(text=button_text,
                                 callback_data=callback_data)
        )

    return markup


async def shares_keyboard(industry, user):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=1)
    shares = await get_shares(industry)

    for share in shares:
        button_text = f'{share.title} - {share.tiker} - ${share.price}'
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           industry=industry,
                                           tiker=share.tiker,
                                           user=int(user)
                                           )
        markup.insert(
            InlineKeyboardButton(text=button_text,
                                 callback_data=callback_data)
        )


    markup.row(
            InlineKeyboardButton(
                text="Назад",
                callback_data=make_callback_data(level=CURRENT_LEVEL-1,
                                                 industry=industry,
                                                 user=user
                                                 )
            )
        )

    return markup

# Создаем функцию, которая отдает клавиатуру с кнопками "купить" и "назад" для выбранного товара
async def share_keyboard(industry, tiker, user):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=2)
    balance_share = await count_operations_by_tiker(user, tiker)

    if balance_share > 0:
        markup.insert(
            InlineKeyboardButton(
                text=f"Купить",
                callback_data=do_operation.new(industry=industry,
                                               tiker=tiker,
                                               user=user,
                                               type='buy'))

        )
        markup.insert(
            InlineKeyboardButton(
                text=f"Продать",
                callback_data=do_operation.new(industry=industry,
                                               tiker=tiker,
                                               user=user,
                                               type='sell'))

        )
    else:
        markup.insert(
            InlineKeyboardButton(
                text=f"Купить",
                callback_data=do_operation.new(industry=industry,
                                               tiker=tiker,
                                               user=user,
                                               type='buy'))
        )

    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             industry=industry,
                                             user=user))
    )

    return markup


async def buy_share(industry, tiker, user):
    # CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup(row_width=1)
    #
    # markup.row(
    #     InlineKeyboardButton(
    #         text="Назад",
    #         callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
    #                                          industry=industry,
    #                                          tiker=tiker,
    #                                          user=user))
    # )


    return markup

