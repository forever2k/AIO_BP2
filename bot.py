import asyncio
import logging
import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import BotCommand
from aiogram.utils.executor import start_webhook
import mysql.connector
from random import randint
from aiogram.utils.exceptions import BotBlocked
from app.config_reader import load_config
from app.handlers.common import register_handlers_common


# test_group = -1001153348142
# test = -1001364950026

me = os.getenv('me')

TOKEN = os.getenv('TOKEN')
PROJECT_NAME = os.getenv('PROJECT_NAME')

WEBHOOK_HOST = f'https://{PROJECT_NAME}.herokuapp.com'
WEBHOOK_PATH = '/' + TOKEN
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.environ.get('PORT')


logging.basicConfig(level=logging.DEBUG)

# bot = Bot(token=TOKEN)
# dp = Dispatcher(bot)

# Парсинг файла конфигурации
config = load_config("config/bot.ini")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

dbase = mysql.connector.connect(
        host=os.getenv('myhost'),
        user=os.getenv('myuser'),
        passwd=os.getenv('mypass'),
        port="3306",
        database="bqcbwpmrbqj7ghxx")

cursor = dbase.cursor()

user_data = {}

class User:
    def __init__(self, question):
        self.question = question
        self.answer1 = ''
        self.answer2 = ''
        self.answer3 = ''
        self.answer4 = ''



async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/ask", description="Ask a question"),
        BotCommand(command="/cancel", description="Cancel")
    ]
    await bot.set_my_commands(commands)


async def main():

    print('TUTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT')
    # Регистрация хэндлеров
    register_handlers_common(dp)

    # Установка команд бота
    await set_commands(bot)





@dp.message_handler(commands=['ttt'], state="*")
async def ttt(message: types.Message):
    await message.answer("ееееееееееееееее")


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
    asyncio.run(main())


