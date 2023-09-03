from aiogram.utils.exceptions import ChatNotFound

from src.misc.config import ADMINS_IDS
from src.misc.loader import bot


async def send_admins(message_text: str = "-"):
    """Рассылает всем админам сообщение.

    Args:
        message_text (str, optional): Текст для рассылки. Defaults to "-".
    """
    for admin_id in ADMINS_IDS:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=message_text,
                parse_mode="html"
            )
        except ChatNotFound:
            continue