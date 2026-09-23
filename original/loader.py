import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.fsm.storage.redis import RedisStorage
from data.config import BOT_TOKEN, REDIS_URL

# Logging sozlamalari
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
storage = RedisStorage.from_url(REDIS_URL)
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
session = AiohttpSession(api=TelegramAPIServer.from_base('http://78.46.147.151:8081'), timeout=720)
local_bot = Bot(token=BOT_TOKEN, session=session)
dp = Dispatcher(storage=storage)
