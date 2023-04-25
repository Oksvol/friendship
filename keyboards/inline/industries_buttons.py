from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import industries_callback


# Вариант 2 - с помощью row_width и insert.
industries = InlineKeyboardMarkup(row_width=1)

entertainment = InlineKeyboardButton(text="Развлечения", switch_inline_query_current_chat="Развлечения", callback_data=industries_callback.new(name="entertainment", quantity="1"))
industries.insert(entertainment)

industry = InlineKeyboardButton(text="Промышленность", switch_inline_query_current_chat="Промышленность", callback_data=industries_callback.new(name="industry", quantity="1"))
industries.insert(industry)

agro_industry = InlineKeyboardButton(text="Аграрная промышленность", switch_inline_query_current_chat="Аграрная промышленность", callback_data=industries_callback.new(name="agro_industry", quantity="1"))
industries.insert(agro_industry)

war_industry = InlineKeyboardButton(text="Военная промышленность", switch_inline_query_current_chat="Военная промышленность", callback_data=industries_callback.new(name="war_industry", quantity="1"))
industries.insert(war_industry)

law = InlineKeyboardButton(text="Юриспруденция", switch_inline_query_current_chat="Юриспруденция", callback_data=industries_callback.new(name="law", quantity="1"))
industries.insert(law)

resources = InlineKeyboardButton(text="Добыча ресурсов", switch_inline_query_current_chat="Добыча ресурсов", callback_data=industries_callback.new(name="resources", quantity="1"))
industries.insert(resources)

jewelry = InlineKeyboardButton(text="Ювелирное дело", switch_inline_query_current_chat="Ювелирное дело", callback_data=industries_callback.new(name="jewelry", quantity="1"))
industries.insert(jewelry)

cars = InlineKeyboardButton(text="Автомобилестроение", switch_inline_query_current_chat="Автомобилестроение", callback_data=industries_callback.new(name="cars", quantity="1"))
industries.insert(cars)

farma = InlineKeyboardButton(text="Фармацевтика", switch_inline_query_current_chat="Фармацевтика", callback_data=industries_callback.new(name="farma", quantity="1"))
industries.insert(farma)

medicine = InlineKeyboardButton(text="Медицина", switch_inline_query_current_chat="Медицина", callback_data=industries_callback.new(name="medicine", quantity="1"))
industries.insert(medicine)

it = InlineKeyboardButton(text="IT", switch_inline_query_current_chat="IT", callback_data=industries_callback.new(name="it", quantity="1"))
industries.insert(it)

merchant = InlineKeyboardButton(text="Торговля", switch_inline_query_current_chat="Торговля", callback_data=industries_callback.new(name="merchant", quantity="1"))
industries.insert(merchant)
