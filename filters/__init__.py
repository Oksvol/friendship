from aiogram import Dispatcher

from .private_chat import IsPrivate

from . import test_filter

def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsPrivate)