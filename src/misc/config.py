from dotenv import load_dotenv
from typing import List
import os


if not load_dotenv():
    raise Exception("Невозможно прогрузить .env файл. Возможно, он находится не в той директории")


ADMINS_IDS: List[int] = list(map(int, os.getenv("ADMINS_IDS").replace(' ', '').split(",")))
BOT_TOKEN: str = os.getenv("BOT_TOKEN")
APPID: str = os.getenv("APPID")

