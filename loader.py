from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api.db_gino import db
from apscheduler.schedulers.asyncio import AsyncIOScheduler

#from utils.db_api.postgresql import Database
from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler()

__all__ = ["bot", "storage", "dp", "db", "scheduler"]
