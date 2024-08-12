import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import requests

from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('TOKEN')
API_KEY = os.getenv('API_KEY')
bot = Bot(token=TOKEN)
dp = Dispatcher()


def get_weather(city):
    api_key = API_KEY
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        return f"Погода в {city}: {weather}, температура: {temp}°C", None
    else:
        return None, "Город не найден или произошла ошибка."


@dp.message(Command('weather'))
async def weather(message: Message):
    # Извлекаем аргументы после команды /weather
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer('Отправьте команду с названием города, например, /weather Москва')
        return

    city = args[1]

    try:
        weather_info, error = get_weather(city)
        if error:
            await message.answer(error)
        else:
            await message.answer(weather_info)
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer(
        'Этот бот умеет выполнять команды:\n/start - Начало работы\n/help - Справка\n/weather <город> - Узнать погоду в указанном городе')


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Приветики! Я бот, который позволяет узнать погоду.')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


