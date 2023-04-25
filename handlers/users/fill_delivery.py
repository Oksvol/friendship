import dateutil.parser as parser
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from typing import Union

from keyboards.default import sending_items_keyboard, role_choice, yn_keyboard
from keyboards.inline import item_type_choice
from keyboards.inline.item_type_choice import create_item_type_choice_keyboard

from loader import dp
from states.deliveries import Delivery
from utils.db_api.quick_commands import add_sending


@dp.callback_query_handler(text="delivery")
async def create_state_of_delivery(call: types.CallbackQuery):
    text = 'Из какого города вы поедете?'
    await call.message.answer(text=text)
    await call.answer()

    await Delivery.start_city.set()


@dp.message_handler(state=Delivery.start_city)
async def make_op(message: Message, state: FSMContext):
    await state.update_data(user_id=message.from_id)
    await state.update_data(start_city=message.text)
    text = f'Из какой страны вы поедете?'
    await message.answer(text=text)

    await Delivery.start_country.set()


@dp.message_handler(state=Delivery.start_country)
async def make_op(message: Message, state: FSMContext):
    await state.update_data(start_country=message.text)
    text = f'В какой город вы едете (можно также ввести район/регион/остров)?'
    await message.answer(text=text)

    await Delivery.end_point.set()


@dp.message_handler(state=Delivery.end_point)
async def make_op(message: Message, state: FSMContext):
    await state.update_data(end_point=message.text)
    text = f'В какую страну вы едете?'
    await message.answer(text=text)

    await Delivery.end_country.set()


# @dp.message_handler(state=Delivery.end_country)
# async def make_op(message: Message, state: FSMContext):
#     await state.update_data(end_country=message.text)
#     text = f'Будут ли у вас промежуточные точки на маршруте, на которых вы сможете принять/передать груз (пересадки менее 24ч)?\n\n'\
#            'Введите через запятую, если их несколько'
#     await message.answer(text=text)
#
#     await Delivery.between_points.set()


@dp.message_handler(state=Delivery.end_country)
async def make_op(message: Message, state: FSMContext):
    await state.update_data(end_country=message.text)
    text = f'На каком транспорте вы едете?\n\n' \
           'Можно ввести несколько через запятую.'
    await message.answer(text=text)

    await Delivery.transport.set()


@dp.message_handler(state=Delivery.transport)
async def make_op(message: Message, state: FSMContext):
    await state.update_data(transport=message.text)
    data = await state.get_data()
    start_point = data.get("end_point")
    start_country = data.get("end_country")
    text = 'Когда вы будете совершать маршрут?\n\n' \
           'Введите дату и время вылета из первой точки.\n\n' \
           'Например: 12:00, 24.12.22\n\n' \
           f'Обязательно вводите местное время в точке {start_country} {start_point}'
    await message.answer(text=text)

    await Delivery.date_start.set()


@dp.message_handler(state=Delivery.date_start)
async def make_op(message: Message, state: FSMContext):
    await state.update_data(date_start=message.text)
    data = await state.get_data()
    end_point = data.get("end_point")
    end_country = data.get("end_country")
    text = f'Когда вы будете в конечной точке {end_point} и сможете отдать посылку?' \
           'Введите время и дату в формате:' \
           f'9:00, 06.12.23 Обязательно вводите местное время в точке {end_country} {end_point}'

    await message.answer(text=text)

    await Delivery.date_end.set()


# @dp.message_handler(text='kek')
# @dp.message_handler(state=Delivery.date_end)
# async def make_op(message: Message, state: FSMContext):
#     await state.update_data(fio=message.text)
#
#     btns = {"small_item": "документы/бумаги/ключи",
#             "middle_item": "Размером менее 25х20х10 и менее 2,5 кг",
#             "big_item": "Размером до 40х25х15 и менее 5 кг",
#             "huge_item": "Размером до 45х35х25 и менее 10 кг",
#             "extra_item": "Дополнительный крупный чемодан",
#             "ready": "Готово",
#             "next": "Отмена"}
#
#     item_type_choice_keyboard = await create_item_type_choice_keyboard(btns)
#
#     # for i in item_type_choice_keyboard["inline_keyboard"]:
#     #     print(i[0]['text'])
#
#     text = 'Какой груз вы бы могли взять с собой для перевозки?' \
#            'Отметьте типы, которые можете взять'
#     await message.answer(text=text, reply_markup=item_type_choice_keyboard[0])
#
#
# @dp.message_handler(text='small_item')
# async def make_op(message: Message, state: FSMContext):
#     await state.update_data(fio=message.text)
#
#     btns = {"small_item": "документы/бумаги/ключи",
#             "middle_item": "Размером менее 25х20х10 и менее 2,5 кг",
#             "big_item": "Размером до 40х25х15 и менее 5 кг",
#             "huge_item": "Размером до 45х35х25 и менее 10 кг",
#             "extra_item": "Дополнительный крупный чемодан",
#             "ready": "Готово",
#             "next": "Отмена"}
#
#     item_type_choice_keyboard = await create_item_type_choice_keyboard(btns)
#
#     # for i in item_type_choice_keyboard["inline_keyboard"]:
#     #     print(i[0]['text'])
#
#     text = 'Какой груз вы бы могли взять с собой для перевозки?' \
#            'Отметьте типы, которые можете взять'
#     await message.answer(text=text, reply_markup=item_type_choice_keyboard[0])


@dp.message_handler(state=Delivery.date_end)
async def make_op(message: Message, state: FSMContext):
    await state.update_data(date_end=message.text)
    text = 'Какой груз вы бы могли взять с собой для перевозки?' \
           'Сможете отвезти документы/бумаги/ключи и другие небольшие вещи, занимающие мало места?'

    await message.answer(text=text, reply_markup=yn_keyboard)
    await Delivery.small_item.set()


@dp.message_handler(state=Delivery.small_item, text='Да')
async def make_op(message: Message, state: FSMContext):
    await state.update_data(small_item=message.text)
    text = 'Сколько вы хотите получить за перевозку такого груза.\n\n'\
           'Напишите стоимость “от”'

    await message.answer(text=text)
    await Delivery.small_item_price.set()


@dp.message_handler(state=Delivery.small_item_price)
@dp.message_handler(state=Delivery.small_item, text="Нет")
async def make_op(message: Message, state: FSMContext):
    await state.update_data(small_item_price=message.text)
    text = 'Сможете взять к перевозке небольшую посылку, размером с толстую книгу?\n'\
           'Размером менее 25х20х10 и менее 2,5 кг?'

    await message.answer(text=text)
    await Delivery.middle_item.set()


@dp.message_handler(state=Delivery.middle_item, text="Да")
async def make_op(message: Message, state: FSMContext):
    await state.update_data(middle_item=message.text)
    text = 'Сколько вы хотите получить за перевозку такого груза.\n\n'\
           'Напишите стоимость “от”'

    await message.answer(text=text)
    await Delivery.middle_item_price.set()


@dp.message_handler(state=Delivery.middle_item_price)
@dp.message_handler(state=Delivery.middle_item, text="Нет")
async def make_op(message: Message, state: FSMContext):
    await state.update_data(middlee_item_price=message.text)
    text = 'Сможете взять к перевозке среднюю посылку, размером коробку из под кроссовок?'\
           'Размером до 40х25х15 и менее 5 кг?'

    await message.answer(text=text)
    await Delivery.big_item.set()


@dp.message_handler(state=Delivery.big_item, text="Да")
async def make_op(message: Message, state: FSMContext):
    await state.update_data(big_item=message.text)
    text = 'Сколько вы хотите получить за перевозку такого груза.\n\n'\
           'Напишите стоимость “от”'

    await message.answer(text=text)
    await Delivery.big_item_price.set()


@dp.message_handler(state=Delivery.big_item_price)
@dp.message_handler(state=Delivery.big_item, text="Нет")
async def make_op(message: Message, state: FSMContext):
    await state.update_data(big_item_price=message.text)
    text = 'Сможете взять к перевозе крупную посылку, размером с чемодан для ручной клади?\n\n'\
           'Размером до 45х35х25 и менее 10 кг?'

    await message.answer(text=text)
    await Delivery.huge_item.set()


@dp.message_handler(state=Delivery.huge_item, text="Да")
async def make_op(message: Message, state: FSMContext):
    await state.update_data(huge_item=message.text)
    text = 'Сколько вы хотите получить за перевозку такого груза.\n\n'\
           'Напишите стоимость “от”'

    await message.answer(text=text)
    await Delivery.huge_item_price.set()


@dp.message_handler(state=Delivery.huge_item_price)
@dp.message_handler(state=Delivery.huge_item, text="Нет")
async def make_op(message: Message, state: FSMContext):
    await state.update_data(huge_item_price=message.text)
    text = 'Сможете взять к перевозке дополнительный крупный чемодан? Для сдачи в багаж, если летите самолетом.'

    await message.answer(text=text)
    await Delivery.extra_item.set()


@dp.message_handler(state=Delivery.extra_item, text="Да")
async def make_op(message: Message, state: FSMContext):
    await state.update_data(extra_item=message.text)
    text = 'Сколько вы хотите получить за перевозку такого груза.\n\n'\
           'Напишите стоимость “от”'

    await message.answer(text=text)
    await Delivery.extra_item_price.set()


@dp.message_handler(state=Delivery.extra_item_price)
@dp.message_handler(state=Delivery.extra_item, text="Нет")
async def make_op(message: Message, state: FSMContext):
    await state.update_data(extra_item_price=message.text)
    text = 'Введите ваши ФИО. Можно без отчества'

    await message.answer(text=text)
    await Delivery.fio.set()


@dp.message_handler(state=Delivery.fio)
async def make_op(message: Message, state: FSMContext):
    await state.update_data(receiver_fio=message.text)
    username = message.from_user.username
    data = await state.get_data()
    user_id = data.get("user_id")
    start_city = data.get("start_city")
    start_country = data.get("start_country")
    end_point = data.get("end_point")
    end_country = data.get("end_country")
    item_type = data.get("item_type")
    date_receiving = parser.parse(data.get("date_receiving"), dayfirst=True).date()
    print(date_receiving)
    fio = data.get("fio")
    role = data.get("role")
    receiver_fio = data.get("receiver_fio")
    text = 'Все готово. Сейчас мы начнем искать перевозчика для вашей посылки.\n\n' \
           'Проверьте вашу отправку.' \
           f'{data}'

    await add_sending(user_id=user_id, full_name=fio,
                      send_from=f"{start_city}, {start_country}", send_to=f"{end_point}, {end_country}",
                      delivery_date=date_receiving, receiver_fio=receiver_fio, item_type=item_type, username=username)

    await message.answer(text=text)

    await Delivery.receiver_fio.set()
