from aiogram.types import InlineQuery

from src.misc.loader import dp, bot, logger
from src.handlers.inline_content import get_inline_query_result

@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    logger.info("InlineQuery from user: %d", inline_query.from_user.id)
    if not inline_query.location:
        logger.info("InlineQuery from user: %d, no permission to send location", inline_query.from_user.id)
        return
    
    location = inline_query.location
    
    await bot.answer_inline_query(
        inline_query.id,
        results=await get_inline_query_result(location),
        cache_time=3600,  # Кешируем результаты на 1 час
        is_personal=True,  # Кешируем рузультаты для каждого пользователя персонально
    )