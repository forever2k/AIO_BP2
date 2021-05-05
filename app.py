import logging
import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
import mysql.connector


test_group = -1001153348142
test = -1001364950026
me = os.getenv('me')



TOKEN = os.getenv('TOKEN')
PROJECT_NAME = os.getenv('PROJECT_NAME')

WEBHOOK_HOST = f'https://{PROJECT_NAME}.herokuapp.com'
WEBHOOK_PATH = '/' + TOKEN
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.environ.get('PORT')


logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


db = mysql.connector.connect(
        host=os.getenv('myhost'),
        user=os.getenv('myuser'),
        passwd=os.getenv('mypass'),
        port="3306",
        database="eyefvtclr0ydnawm")


# print(db)
# print(db)

cursor = db.cursor()

user_data = {}


@dp.message_handler(commands=['start'])
async def main_start(message: types.Message):
    await message.answer("Bot aio-bp2 works")



        


async def on_startup(dp):
    logging.warning('Starting connection')
    await bot.set_webhook(WEBHOOK_URL)
    # asyncio.create_task(bot_schedule())


async def on_shutdown(dp):
    logging.warning('Bye! Shutting down webhook connection')


if __name__ == '__main__':
    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
                  on_startup=on_startup, on_shutdown=on_shutdown,
                  host=WEBAPP_HOST, port=WEBAPP_PORT, skip_updates=True)

