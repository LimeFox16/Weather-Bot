from aiogram import types

from src.misc.loader import dp, bot


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text="<i>Попробуй вписать мой никнейм в <b>любой чат</b> телеграмма</i>",
        parse_mode="HTML"
    )
    
