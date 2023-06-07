import json
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hlink
from aiogram.dispatcher.filters import Text

from main import check_news_update
from config import TOKEN, CHAT_ID

chat_id = CHAT_ID
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    start_buttons = ['Hamma yangiliklar', 'Oxirgi 5 yangilik', 'Yangi yangiliklar']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Assalomu alaykum, yangiliklar bilan tanishing', reply_markup=keyboard)


@dp.message_handler(Text(equals='Hamma yangiliklar'))
async def get_all_news(message: types.Message):
    with open('news.json', 'r') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):
        news = f'{hbold(v["date"])}\n{hlink(v["text"], v["link"])}'

        await message.answer(news)


@dp.message_handler(Text(equals='Oxirgi 5 yangilik'))
async def get_last_five_news(message: types.Message):
    with open('news.json', 'r') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = f'{hbold(v["date"])}\n{hlink(v["text"], v["link"])}'

        await message.answer(news)


@dp.message_handler(Text(equals='Yangi yangiliklar'))
async def get_fresh_news(message: types.Message):
    fresh_news = check_news_update()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f'{hbold(v["date"])}\n{hlink(v["text"], v["link"])}'

            await message.answer(news)
    else:
        await message.answer('Yangiliklar yo\'q')


async def news_every_5_minutes():
    while True:
        fresh_news = check_news_update()

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news = f'{hbold(v["date"])}\n{hlink(v["text"], v["link"])}'

                await bot.send_message(chat_id=chat_id, text=news)

        await asyncio.sleep(300)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_5_minutes())
    executor.start_polling(dp)