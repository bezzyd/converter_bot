import logging
import os
import asyncio
from aiohttp import ClientSession

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types

load_dotenv()

API_TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def choose_currency(message: types.Message):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True, row_width=2
        )
    eur_button = types.InlineKeyboardButton(text="EUR")
    usd_button = types.InlineKeyboardButton(text="USD")
    cny_button = types.InlineKeyboardButton(text="CNY")
    try_button = types.InlineKeyboardButton(text="TRY")
    byn_button = types.InlineKeyboardButton(text="BYN")
    kzt_button = types.InlineKeyboardButton(text="KZT")
    markup.add(
        eur_button, usd_button, cny_button,
        try_button, byn_button, kzt_button
        )
    await message.answer(
        f"Привет, {message.from_user.first_name} 👋\n" +
        "Я могу показать тебе курсы валют ЦБ РФ.\n" +
        "Чтобы узнать курс нужной тебе валюты просто выбери её 😎",
        reply_markup=markup)


@dp.message_handler(commands=["help"])
async def help(message: types.Message):
    await message.answer(
        f"{message.from_user.first_name}, " +
        "помощь не предусмотрена 😥"
        )


# data = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()


async def get_data():
    async with ClientSession() as session:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"

        async with session.get(url) as response:
            return await response.json()


@dp.message_handler(content_types="text")
async def eur_rate(message: types.Message):
    if message.text == "EUR":
        await message.answer(
            "Курс евро на данный момент - " +
            f"{await get_data()['Valute']['EUR']['Value']} 🙄"
            )


@dp.message_handler(content_types="text")
async def usd_rate(message: types.Message):
    if message.text == "USD":
        await message.answer(
            "Курс американского доллара на данный момент - " +
            f"{data['Valute']['USD']['Value']} 🙄"
            )


@dp.message_handler(content_types="text")
async def cny_rate(message: types.Message):
    if message.text == "CNY":
        await message.answer(
            "Курс китайского юаня на данный момент - " +
            f"{data['Valute']['CNY']['Value']} 🙄"
            )


@dp.message_handler(content_types="text")
async def try_rate(message: types.Message):
    if message.text == "TRY":
        await message.answer(
            "Курс турецкой лиры на данный момент - " +
            f"{data['Valute']['TRY']['Value']} 🙄"
            )


@dp.message_handler(content_types="text")
async def byn_rate(message: types.Message):
    if message.text == "BYN":
        await message.answer(
            "Курс белорусского рубля на данный момент - " +
            f"{data['Valute']['BYN']['Value']} 🙄"
            )


@dp.message_handler(content_types="text")
async def kzt_rate(message: types.Message):
    if message.text == "KZT":
        await message.answer(
            "Курс казахского тенге на данный момент - " +
            f"{data['Valute']['KZT']['Value']} 🙄"
            )


@dp.message_handler()
async def no_way(message: types.Message):
    await message.answer("Других валют не завезли. И кто в этом виноват? 🤪")

if __name__ == '__main__':
    asyncio.run(get_data())
    executor.start_polling(dp, skip_updates=True)
