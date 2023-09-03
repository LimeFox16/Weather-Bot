# - *- coding: utf- 8 - *-
from aiogram import executor, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from src.handlers import dp
from src.misc.loader import bot
from src.utils.tools import send_admins


async def set_commands():
    user_commands = [
        BotCommand("start", "▶️ Главное меню"),
    ]
    await bot.set_my_commands(user_commands, scope=BotCommandScopeDefault())

async def on_startup(dp: Dispatcher):
    await send_admins("Бот запущен")
    await set_commands()
        
async def on_shutdown(dp: Dispatcher):
    await send_admins("Бот остановлен")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
