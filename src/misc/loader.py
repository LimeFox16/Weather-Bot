# - *- coding: utf- 8 - *-
from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import time

from src.misc.config import BOT_TOKEN


def get_logger():
    logging.basicConfig(level = logging.INFO)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    handler = logging.FileHandler(fr"logging//{time.strftime('%Y_%m_%d-%H_%M_%S', time.localtime())}.log", 'w', 'utf-8')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    
    return root_logger

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
logger = get_logger()