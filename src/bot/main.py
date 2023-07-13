import logging
import os
import json
import decimal
import aiohttp
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
        resize_keyboard=True, row_width=2
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


async def get_data():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.cbr-xml-daily.ru/daily_json.js") as response:
            data = await response.read()
            return json.loads(data)


@dp.message_handler(lambda message: message.text == "EUR")
async def eur_rate(message: types.Message):
    task = await get_data()
    await message.answer(
        "Курс евро на данный момент - " +
        f"{round(task['Valute']['EUR']['Value'], 2)} 🙄"
        )


@dp.message_handler(lambda message: message.text == "USD")
async def usd_rate(message: types.Message):
    task = await get_data()
    await message.answer(
        "Курс американского доллара на данный момент - " +
        f"{round(task['Valute']['USD']['Value'], 2)} 🙄"
        )


@dp.message_handler(lambda message: message.text == "CNY")
async def cny_rate(message: types.Message):
    task = await get_data()
    await message.answer(
        "Курс китайского юаня на данный момент - " +
        f"{round(task['Valute']['CNY']['Value'], 2)} 🙄"
        )


@dp.message_handler(lambda message: message.text == "TRY")
async def try_rate(message: types.Message):
    task = await get_data()
    await message.answer(
        "Курс турецкой лиры на данный момент - " +
        f"{round(decimal.Decimal(task['Valute']['TRY']['Value']) / decimal.Decimal(10), 2)} 🙄"
        )


@dp.message_handler(lambda message: message.text == "BYN")
async def byn_rate(message: types.Message):
    task = await get_data()
    await message.answer(
        "Курс белорусского рубля на данный момент - " +
        f"{round(task['Valute']['BYN']['Value'], 2)} 🙄"
        )


@dp.message_handler(lambda message: message.text == "KZT")
async def kzt_rate(message: types.Message):
    task = await get_data()
    await message.answer(
        "Курс казахского тенге на данный момент - " +
        f"{round(decimal.Decimal(task['Valute']['KZT']['Value']) / decimal.Decimal(100), 2)} 🙄"
        )


@dp.message_handler()
async def answer_for_other_messages(message: types.Message):
    await message.answer("Других валют не завезли. И кто в этом виноват? 🤪")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
