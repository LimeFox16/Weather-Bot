from typing import Literal
import aiohttp
import datetime
import time

from src.misc.config import APPID


class Weather:
    def __init__(self, latitude: str, longitude: str) -> None:
        self.lat = latitude
        self.lon = longitude
    
    async def get_response_data(self) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url = 'http://api.openweathermap.org/data/2.5/forecast',
                params={
                    'lat': self.lat,
                    'lon': self.lon,
                    'units': 'metric',
                    'lang': 'ru',
                    'appid': APPID
                }
            ) as response:
                resp_data = await response.json()
        print(resp_data['list'][-1]["dt_txt"])   
        return resp_data

    async def weather_info_today(self, data: dict) -> str:
        weather_info = data['list'][0]
        
        rainy, snowy = weather_info.get('rain'), weather_info.get('snow')
        if rainy:
            rainy = f"\n• <i>Дождь:</i> <u>{rainy['3h']}</u> мм."
        if snowy:
            snowy = f"\n• <i>Снег:</i> <u>{snowy['3h']}</u> мм."
        precipitations = rainy + snowy if rainy and snowy else rainy or snowy or ""
            
        text = f"""
🗓️ <b>{await self.get_time_by_int(weather_info['dt'], data['city']['timezone'], '%H:%M, %d.%m.%Yг.')}</b>
⛅ <b>Погода:</b> <u>{weather_info['weather'][0]['description']}</u>
🌡️ <b>Температура:</b>
    • <u>{weather_info['main']['temp']}</u>°C
    • <i>Ощущается как</i> <u>{weather_info['main']['feels_like']}</u>°C
💨 <b>Ветер:</b>
    • <i>Скорость:</i> <u>{weather_info['wind']['speed']}</u> м/c
    • <i>Направление:</i> <u>{await self.get_direction_by_deg(weather_info['wind']['deg'])}</u>
🗂️ <b>Другое:</b>
    • <i>Давление:</i> <b><u>{weather_info['main']['pressure']}</u></b> мм.рт.ст.
    • <i>Влажность:</i> <u>{weather_info['main']['humidity']}</u>%{precipitations}
    • <i>Рассвет:</i> <u>{await self.get_time_by_int(data['city']['sunrise'], data['city']['timezone'])}</u>
    • <i>Закат:</i> <u>{await self.get_time_by_int(data['city']['sunset'], data['city']['timezone'])}</u>
"""
        return text
    
    async def weather_info_by_day(self, data: dict, days: int) -> str:
        text = ""
        
        for i, weather_info in enumerate(data["list"]):
            if time.gmtime(weather_info["dt"]).tm_hour != 12 or time.gmtime(weather_info["dt"]).tm_mday == time.gmtime(time.time()).tm_mday:
                continue
            
            text += f"""
🗓️ {await self.get_time_by_int(weather_info["dt"], data['city']['timezone'], '%d.%m.%Yг.')}
⛅ <b>Погода:</b> <u>{weather_info['weather'][0]['description']}</u>
🌡️ <b>Температура:</b> <u>{weather_info['main']['temp']}</u>°C
💨 <b>Ветер:</b> <u>{await self.get_direction_by_deg(weather_info['wind']['deg'])}</u> - <u>{weather_info['wind']['speed']}</u> м/c
"""
            if i + 1 > days * 8:
                break
        return text
    
    async def detailed_weather_info(self, data: dict, days_after: int = 1) -> str:
        next_day = datetime.date.today() + datetime.timedelta(days=days_after)
        
        text = f"🗓️ {datetime.datetime.strftime(next_day, '%d.%m.%Yг.')}\n"
        for i, weather_info in enumerate(data["list"]):
            rainy, snowy = weather_info.get('rain'), weather_info.get('snow')
            if rainy:
                rainy = f"\n🌧 <i>Дождь:</i> <u>{rainy['3h']}</u> мм.💧"
            if snowy:
                snowy = f"\n❄️ <i>Снег:</i> <u>{snowy['3h']}</u> мм."
            precipitations = rainy + snowy if rainy and snowy else rainy or snowy or ""
            
            if time.gmtime(weather_info["dt"]).tm_mday != next_day.day:
                continue
            
            text += f"""
🕑 <b>{await self.get_time_by_int(weather_info["dt"], data['city']['timezone'], '%H:%M')}</b>
⛅ <i>Погода:</i> <u>{weather_info['weather'][0]['description']}</u>
🌡️ <i>Температура:</i> <u>{weather_info['main']['temp']}</u>°C
💨 <i>Ветер:</i> <u>{await self.get_direction_by_deg(weather_info['wind']['deg'])}</u> - <u>{weather_info['wind']['speed']}</u> м/c
☁️ <i>Облачность:</i> <u>{weather_info['clouds']['all']}</u>%{precipitations}
"""
        return text
    
    @staticmethod
    async def get_time_by_int(num: int, timezone: int = 0, format: str = '%H:%M:%S') -> str:
        """Получить отформатированную строку времени по числу

        Args:
            num (int): Число секунд.
            timezone (int, optional): Смещение времени в секундах. Defaults to 0.
            format (_type_, optional): Строка под форматирование. Defaults to '%H:%M:%S'.

        Returns:
            str: Отформатированная строка времени.
        """
        return time.strftime(format, time.gmtime(num + timezone))

    @staticmethod
    async def get_direction_by_deg(deg: int) -> Literal['С', 'СВ', 'В', 'ЮВ', 'Ю', 'ЮЗ', 'З', 'СЗ']:
        deg = deg % 360
        if 342.5 < deg or deg <= 27.5:
            return 'С'
        elif 27.5 < deg <= 72.5:
            return 'СВ'
        elif 72.5 < deg <= 117.5:
            return 'В'
        elif 117.5 < deg <= 162.5:
            return 'ЮВ'
        elif 162.5 < deg <= 207.5:
            return 'Ю'
        elif 207.5 < deg <= 252.5:
            return 'ЮЗ'
        elif 252.5 < deg <= 297.5:
            return 'З'
        elif 297.5 < deg <= 342.5:
            return 'СЗ'
