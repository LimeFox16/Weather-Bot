from aiogram.types import InputTextMessageContent, InlineQueryResultArticle, location
import datetime

from src.utils.weather import Weather


async def get_inline_query_result(location: location.Location) -> list:
    weather = Weather(location.latitude, location.longitude)
    data = await weather.get_response_data()
    today = datetime.date.today()
    next_day = lambda days_plus: today + datetime.timedelta(days=days_plus)
    
    inline_query_data = {
        1: {
            'message_text': await weather.weather_info_today(data),
            'title': 'Погода на сегодня',
            'description': 'Узнай погоду на сегодня',
            'thumb_url': f'https://img.icons8.com/fluency/48/calendar-{today.day}.png'
        },
        2: {
            'message_text': await weather.weather_info_by_day(data, 1),
            'title': 'Погода на завтра',
            'description': 'Узнай погоду на завтра',
            'thumb_url': f'https://img.icons8.com/fluency/48/calendar-{next_day(1).day}.png'
        },
        3: {
            'message_text': await weather.weather_info_by_day(data, 3),
            'title': 'Погода на 3 дня',
            'description': 'Узнай погоду на ближайшие 3 дня',
            'thumb_url': f'https://img.icons8.com/fluency/48/calendar-{next_day(2).day}.png'
        },
        4: {
            'message_text': await weather.weather_info_by_day(data, 5),
            'title': 'Погода на 5 дней',
            'description': 'Узнай погоду на ближайшие 5 дней',
            'thumb_url': f'https://img.icons8.com/fluency/48/calendar-{next_day(4).day}.png'
        },
        5: {
            'message_text': await weather.detailed_weather_info(data, 0),
            'title': 'Детальный прогноз на сегодня',
            'description': 'Получи детальный прогноз на оставшееся время сегодня',
            'thumb_url': 'https://img.icons8.com/fluency/48/plus-1hour.png'
        },
        6: {
            'message_text': await weather.detailed_weather_info(data, 1),
            'title': 'Детальный прогноз на завтра',
            'description': 'Получи детальный прогноз на завтра по часам',
            'thumb_url': 'https://img.icons8.com/fluency/48/plus-1day.png'
        },
    }
    
    items = []
    for i in range(1, len(inline_query_data) + 1):
        input_content = InputTextMessageContent(
            message_text=inline_query_data[i]["message_text"],
            parse_mode="html"
        )
        item = InlineQueryResultArticle(
            id=str(i),
            title=inline_query_data[i]["title"],
            description=inline_query_data[i]["description"],
            input_message_content=input_content,
            thumb_url=inline_query_data[i]["thumb_url"]
        )
        items.append(item)
    
    return items