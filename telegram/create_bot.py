from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import os, asyncio, pytz

moscow_tz = pytz.timezone('Europe/Moscow')

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
config.bot_id = bot.id

memory_storage = MemoryStorage()
dp = Dispatcher(storage=memory_storage)