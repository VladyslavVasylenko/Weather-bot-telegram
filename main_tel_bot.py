import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
  await message.reply("Привіт! Напиши мені назву міста і я надішлю тобі погоду на сьгодні!")


@dp.message_handler()
async def get_weather(message: types.Message):
  code_to_smile = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Хмарно \U00002601",
    "Rain": "Дощ \U00002614",
    "Drizzle": "Дощ \U00002614",
    "Thunderstorm": "Гроза \U000026A1",
    "Snow": "Сніг \U0001F328",
    "Mist": "Туман \U0001F32B"
  }

  try:
    r = requests.get(
      f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
      )
    data = r.json()

    city = data["name"]
    cur_weather = data["main"]["temp"]

    weather_description = data["weather"][0]["main"]
    if weather_description in code_to_smile:
      wd = code_to_smile[weather_description]
    else:
      wd = "Подивися у вікно, не зрозумію, що там за погода!"

    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind = data["wind"]["speed"]
    sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
    sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
    length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
      data["sys"]["sunrise"])

    await message.reply(f"Зараз {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n"
                        f"Погода в місті {city} сьогодні в нас {wd}\n"
                        f'\n'
                        f"Температура: {cur_weather}°C\nВологість: {humidity}%\nТиск: {pressure}\nВітер: {wind} метрів в секунду\n"
                        f'\n'
                        f"Схід сонця: {sunrise_timestamp}\nЗахід сонця: {sunset_timestamp}\nТривалість дня: {length_of_the_day}\n"
                        f'\n'
                        f"Гарного вам дня!"
                          )

  except:
    await message.reply("\U00002620 Ви ввели не правельно назву міста! \U00002620")


if __name__ == '__main__':
  executor.start_polling(dp)
