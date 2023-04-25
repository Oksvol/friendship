from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from keyboards.default import sending_items_keyboard, role_choice
from loader import dp
from aiogram import types

from states.sendings import Sending
from utils.db_api.quick_commands import add_sending
import dateutil.parser as parser


@dp.callback_query_handler(text="sending")
async def create_state_of_sending(call: types.CallbackQuery):
    text = 'Из какого города вы хотите отправить посылку?'
    await call.message.answer(text=text)
    await call.answer()

    await Sending.start_city.set()


@dp.message_handler(state=Sending.start_city)
async def make_op(message: Message, state: FSMContext):
    await state.update_data(user_id=message.from_id)
    await state.update_data(start_city=message.text)
    text = f'Из какой страны вы хотите отправить посылку?'
    await message.answer(text=text)

    await Sending.start_country.set()


@dp.message_handler(state=Sending.start_country)
async def make_op(message: Message, state: FSMContext):
    await state.update_data(start_country=message.text)
    text = f'В какой город (можно также ввести район/регион/остров)?'
    await message.answer(text=text)

    await Sending.end_point.set()


@dp.message_handler(state=Sending.end_point)
async def make_op(message: Message, state: FSMContext):
    await state.update_data(end_point=message.text)
    text = f'В какую страну вы хотите отправить посылку?'
    await message.answer(text=text)

    await Sending.end_country.set()


@dp.message_handler(state=Sending.end_country)
async def make_op(message: Message, state: FSMContext):
    await state.update_data(end_country=message.text)
    text = f'Что вы хотите отправить?'
    await message.answer(text=text, reply_markup=sending_items_keyboard)

    await Sending.item_type.set()


@dp.message_handler(state=Sending.item_type)
async def make_op(message: Message, state: FSMContext):
    item_type = message.text
    if item_type == "Документы/ключи/бумаги":
        await state.update_data(item_type=item_type)
        text = 'Какой крайний срок получения посылки в стране, куда ее нужно отправить? Введите дату в формате ДД.ММ.ГГ' \
               '(до какого числа хотите получить груз) Если посылка еще не готова к отправке и вы сможете отправить ее ' \
               'только позже, то напишите диапазон дат в формате ДД.ММ.ГГ-ДД.ММ.ГГ'
        await Sending.date_receiving.set()
    elif item_type == "Личные вещи":
        text = 'Опишите, что именно вы везете и укажите примерный размер и вес.\n\n'\
               'Например: Банка соленых огурцов, 2 кг, размер 30х15х15, стекло'
        await Sending.item_type.set()
    elif item_type == "Другое":
        text = 'Опишите, что именно вы везете и укажите примерный размер и вес.\n\n'\
               'Например: Банка соленых огурцов, 2 кг, размер 30х15х15, стекло'
        await Sending.item_type.set()
    else:
        text = 'Какой крайний срок получения посылки в стране, куда ее нужно отправить? Введите дату в формате ДД.ММ.ГГ ' \
               '(до какого числа хотите получить груз) Если посылка еще не готова к отправке и вы сможете отправить ее ' \
               'только позже, то напишите диапазон дат в формате ДД.ММ.ГГ-ДД.ММ.ГГ'

        await Sending.date_receiving.set()

    await message.answer(text=text)


@dp.message_handler(state=Sending.date_receiving)
async def make_op(message: Message, state: FSMContext):
    await state.update_data(date_receiving=message.text)
    text = 'Введите ваше Имя Фамилию. (Можно без отчества)'
    await message.answer(text=text)

    await Sending.fio.set()


@dp.message_handler(state=Sending.fio)
async def make_op(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    text = 'Вы будете отправлять или получать посылку?'
    await message.answer(text=text, reply_markup=role_choice)

    await Sending.role.set()


@dp.message_handler(state=Sending.role)
async def make_op(message: Message, state: FSMContext):
    role = message.text
    await state.update_data(role=message.text)
    text = 'Введите ФИО получателя. Можно без отчества'
    await message.answer(text=text)

    await Sending.receiver_fio.set()


@dp.message_handler(state=Sending.receiver_fio)
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
    fio = data.get("fio")
    role = data.get("role")
    receiver_fio = data.get("receiver_fio")
    text = 'Все готово. Сейчас мы начнем искать перевозчика для вашей посылки.\n\n' \
           'Проверьте вашу отправку.' \
           f'{data}'

    await message.answer(text=text)

    await add_sending(user_id=user_id, full_name=fio,
                      send_from=f"{start_city}, {start_country}", send_to=f"{end_point}, {end_country}",
                      delivery_date=date_receiving, receiver_fio=receiver_fio, item_type=item_type, username=username)
    await state.finish()



    
