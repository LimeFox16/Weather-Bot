from src.misc.loader import dp, bot
from aiogram import types


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text="<i>Попробуй вписать мой никнейм в <b>любой чат</b> телеграмма</i>",
        parse_mode="HTML"
    )
    
