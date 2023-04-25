import logging
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, message

from typing import Union

from aiogram.dispatcher.filters import Command, Text

from handlers.users.news import bot_news
from handlers.users.portfel import bot_portfel
from handlers.users.start import bot_start
from keyboards.inline.industries_btns import industries_keyboard, shares_keyboard, menu_cd, share_keyboard, \
    buy_share, do_operation
from loader import dp
from states.operations import Operation

from utils.db_api.quick_commands import select_industry, get_share, select_user, \
    add_operation, update_share_quantity
from utils.misc.count_balance import show_balance
from utils.misc.count_share_balance import count_operations_by_tiker
from utils.misc.prettifying import money_format, grades_format
from utils.misc.random_price import rand_prices


@dp.message_handler(Text(equals=["Биржа"]))
@dp.message_handler(Command('exchange'))
async def bot_exchange(message: Message):
    # Выполним функцию, которая отправит пользователю кнопки с доступными категориями
    await list_industries(message)


# Та самая функция, которая отдает категории. Она может принимать как CallbackQuery, так и Message
# Помимо этого, мы в нее можем отправить и другие параметры - category, subcategory, item_id,
# Поэтому ловим все остальное в **kwargs
async def list_industries(message: Union[Message, CallbackQuery], **kwargs):
    user = int(message.from_user.id)
    # Клавиатуру формируем с помощью следующей функции (где делается запрос в базу данных)
    markup = await industries_keyboard(user)

    # Проверяем, что за тип апдейта. Если Message - отправляем новое сообщение
    if isinstance(message, Message):
        await message.answer(f"Загружаю данные биржи...")
        await rand_prices()

        await message.answer(f"Биржа – это основной инструмент игры. \n"
                             f"Здесь ты можешь покупать ценные бумаги, чтобы обогатиться и раскачать капитал. \n\n"
                             f"Все компании поделены по отраслям. \n\n"
                             f"Выбирай отрасль и внутри будет список компаний. Купить можно сколько угодно, но не больше, чем позволяет твой капитал.\n\n"
                             f"Если у тебя уже есть акции компании, то их можно продать по текущей цене.", reply_markup=markup)


    # Если CallbackQuery - изменяем это сообщение
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)

async def list_shares(callback: CallbackQuery, industry, user, **kwargs):

    markup = await shares_keyboard(industry, user)
    industry_name = await select_industry(industry)
    await callback.message.edit_text(f"Вот акции из категории {industry_name.title}", reply_markup=markup)


# Функция, которая отдает уже кнопку Купить акцию по выбранному тикеру
async def show_share(callback: CallbackQuery,industry, tiker, user):
    markup = await share_keyboard(industry, tiker, user)
    balance_share = await count_operations_by_tiker(user, tiker)

    # Берем запись о нашей акции из базы данных
    share = await get_share(tiker)

    if balance_share > 0:
        text = f"<b>{share.title} - {share.tiker}</b> \n\n<b>Цена: ${share.price}</b> \n\n<b>Есть в портфеле: {balance_share} шт.</b> \n\n<i>{share.description}</i>"
    else:
        text = f"<b>{share.title} - {share.tiker}</b> \n\n<b>Цена: ${share.price}</b> \n\n<i>{share.description}</i>"

    await callback.message.edit_text(text=text, reply_markup=markup)

# Функция, которая предлагает купить акцию
async def buy_shares(callback: CallbackQuery, industry, tiker, user):
    markup = await buy_share(industry, tiker, user)
    player = await select_user(int(user))
    share = await get_share(tiker)
    balance = await show_balance(int(user))
    allowed_quantity = int(float(balance) / float(share.price))
    text = f'Напиши количество, сколько хочешь купить акций компании "{share.title}" \n\n'\
           f'<b>Денег в твоем кошельке: ${await money_format(balance)}</b> \n'\
           f'<b>Цена за одну акцию: ${await money_format(share.price)}</b> \n\n'\
           f'<b>Максимум ты можешь купить {await grades_format(allowed_quantity)} шт.</b>\n\n' \
           f'<code>ВНИМАНИЕ! Если ты пришлешь число, будет выполнена операция. Для отмены, напиши Отмена</code>'

    state = dp.current_state(user=player.id)
    await callback.message.edit_text(text=text, reply_markup=markup)
    await state.update_data(player=player.id)
    await state.update_data(type='buy')
    await state.update_data(tiker=tiker)
    await state.update_data(allowed_quantity=allowed_quantity)
    await state.update_data(share_title=share.title)
    await state.update_data(industry=industry)
    await state.update_data(price=share.price)
    await Operation.quantity.set()


@dp.message_handler(state=Operation.quantity)
async def make_op(message: Message, state: FSMContext):
    #Достаем переменные
    data = await state.get_data()
    user = data.get("player")
    type = data.get("type")
    tiker = data.get("tiker")
    allowed_quantity = data.get("allowed_quantity")
    share_title = data.get("share_title")
    industry = data.get("industry")
    price = data.get("price")
    quantity = message.text



    try:
        quantity = int(quantity)
    except:
        if quantity.lower() == "Отмена".lower() or quantity.lower() == "Биржа".lower() or quantity.lower() == "/exchange".lower():
            await state.reset_state(with_data=False)
            await bot_exchange(message)
        elif quantity.lower() == "/news".lower() or quantity.lower() == "Новости компаний".lower():
            await state.reset_state(with_data=False)
            await bot_news(message)
        elif quantity.lower() == "/portfel".lower() or quantity.lower() == "Состояние счета".lower():
            await state.reset_state(with_data=False)
            await bot_portfel(message)
        elif quantity.lower() == "/start".lower():
            await state.reset_state(with_data=False)
            await bot_start(message)
        elif type == 'buy' and quantity.lower() != "Отмена".lower():
            text = "Пожалуйста, введи <b>целое число</b>, сколько акций ты хочешь купить"
        elif type == 'sell' and quantity.lower() != "Отмена".lower():
            text = "Пожалуйста, введи <b>целое число</b>, сколько акций ты хочешь продать"

    if isinstance(quantity, int):
        if type == 'buy':
            if quantity <= allowed_quantity and quantity > 0:
                await add_operation(str(user), tiker, type, quantity, industry, price)
                await update_share_quantity(tiker, quantity)
                player_balance = await show_balance(user)

                text = f'Отлично! +{await grades_format(quantity)} акций компании "{share_title}" в твоем портфеле! \n\n' \
                       f'Осталось денег: ${await money_format(player_balance)} \n\n ' \
                       f'Теперь жди новостей на рынке) \n\n ' \
                       f'Чтобы продолжить покупки, нажми /exchange'
                await state.finish()
            elif quantity == 0:
                text = f'0 акций? Урааааа! У нас тут операция на 0 акций) Давай хотя бы одну?'
            elif quantity < 0:
                text = f'Мы тут на позитиве, так что нужны положительные числа)'
            else:
                text = f"Это больше, чем ты можешь себе позволить. Максимальное количество, которое ты можешь купить – {allowed_quantity} шт."

        else:
            if quantity <= allowed_quantity and quantity > 0:
                await add_operation(str(user), tiker, type, quantity, industry, price)
                await update_share_quantity(tiker, quantity)
                player_balance = await show_balance(user)
                text = f'Отлично! Ты продал {await grades_format(quantity)} акций компании "{share_title}" \n\n' \
                       f'Осталось денег: ${await money_format(player_balance)} \n ' \
                       f'Чтобы продолжить совершать сделки, нажми /exchange'
                await state.finish()
            elif quantity == 0:
                text = f'0 акций? Урааааа! У нас тут операция на 0 акций) Давай хотя бы одну?'
            elif quantity < 0:
                text = f'Мы тут на позитиве, так что нужны положительные числа)'
            else:
                text = f"У тебя нет столько акций. Максимальное количество, которое ты можешь продать – {allowed_quantity} шт."

    await message.answer(text=text)


async def sell_shares(callback: CallbackQuery, industry, tiker, user):
    markup = await buy_share(industry, tiker, user)
    player = await select_user(int(user))
    share = await get_share(tiker)
    balance = await show_balance(int(user))
    balance_share = await count_operations_by_tiker(user, tiker)
    text = f'Напиши количество, сколько хочешь продать акций компании "{share.title}" \n\n'\
           f'<b>У тебя есть в кошельке ${await money_format(balance)}</b> \n'\
           f'<b>Цена за одну акцию: ${await money_format(share.price)}</b> \n\n'\
           f'<b>Всего таких акций у тебя в портфеле: {await grades_format(balance_share)} шт.</b>\n\n' \
           f'<code>ВНИМАНИЕ! Если ты пришлешь число, будет выполнена операция. Для отмены, напиши Отмена</code>'

    state = dp.current_state(user=player.id)
    await callback.message.edit_text(text=text, reply_markup=markup)
    await state.update_data(player=player.id)
    await state.update_data(type='sell')
    await state.update_data(tiker=tiker)
    await state.update_data(allowed_quantity=balance_share)
    await state.update_data(share_title=share.title)
    await state.update_data(industry=industry)
    await state.update_data(price=share.price)
    await Operation.quantity.set()


@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    current_level = callback_data.get('level')
    industry = callback_data.get('industry')
    tiker = callback_data.get('tiker')
    user = callback_data.get('user')
    logging.info(f"{callback_data=}")

    levels = {
        "0": list_industries,
        '1': list_shares,
        '2': show_share
    }

    current_level_function = levels[current_level]

    await current_level_function(call, industry=industry, tiker=tiker, user=user)


@dp.callback_query_handler(do_operation.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    type = callback_data.get('type')
    industry = callback_data.get('industry')
    tiker = callback_data.get('tiker')
    user = callback_data.get('user')
    logging.info(f"{callback_data=}")

    types = {
        "buy": buy_shares,
        "sell": sell_shares,
        "back": show_share
    }

    type_function = types[type]

    await type_function(call, industry=industry, tiker=tiker, user=user)




