import asyncio
import logging
import os
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import BotCommand
from aiogram.utils import executor, deep_linking
from aiogram.utils.executor import start_webhook
import mysql.connector
from random import randint
from aiogram.utils.exceptions import BotBlocked
from newapp.config import *
from newapp.handlers.common import *
from newapp.handlers.get_data_from_database import *
from newapp.handlers.get_data_from_user import *
from bt import *


# test_group = -1001153348142
# test = -1001364950026
#
# me = os.getenv('me')
#
# TOKEN = os.getenv('TOKEN')
# PROJECT_NAME = os.getenv('PROJECT_NAME')
#
# WEBHOOK_HOST = f'https://{PROJECT_NAME}.herokuapp.com'
# WEBHOOK_PATH = '/' + TOKEN
# WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
#
# WEBAPP_HOST = '0.0.0.0'
# WEBAPP_PORT = os.environ.get('PORT')


logging.basicConfig(level=logging.DEBUG)

# bot = Bot(token=TOKEN)
# dp = Dispatcher(bot, storage=MemoryStorage())

# Парсинг файла конфигурации

# bot = Bot(token=TOKEN)
# dp = Dispatcher(bot)


# cursor = dbase.cursor()


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/ask", description="Ask a question"),
        BotCommand(command="/cancel", description="Cancel"),
        # BotCommand(command="/rrrr", description="rrrr")

    ]
    await bot.set_my_commands(commands)


dp.register_message_handler(cmd_start, commands="start", state="*")
dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
dp.register_message_handler(ask_start, commands=["ask"], state="*")
dp.register_message_handler(cmd_random, commands=["random"], state="*")
dp.register_message_handler(send_random_value, commands="random_value", state="*")
dp.register_message_handler(secret_command, IDFilter(user_id=me), commands="secret")
dp.register_message_handler(get_question, state=GetData.waiting_for_get_question)
# dp.register_message_handler(ask_answer, state=GetData.waiting_for_ask_answer)
dp.register_message_handler(write_answer, state=GetData.waiting_for_write_answer)
dp.register_message_handler(get_quiz_from_database, state=GetDataFromDatabase.waiting_for_get_session_id)
dp.register_message_handler(send_correct_question, state=GetDataFromDatabase.waiting_for_correct_question)
dp.register_message_handler(send_correct_answer, state=GetDataFromDatabase.waiting_for_correct_answer)
dp.register_message_handler(ask_session_id, IDFilter(user_id=me), commands="asksecret")
dp.register_message_handler(ask_edit_quiz, commands="78978954645756856474758689", state="*")
dp.register_message_handler(check_admin_data, commands="checkdata", state="*")


dp.register_errors_handler(error_bot_blocked, exception=BotBlocked)

dp.register_callback_query_handler(start_session, text="start_session")
dp.register_callback_query_handler(close_session, text="close_session")
dp.register_callback_query_handler(get_answer, text="get_answer")
dp.register_callback_query_handler(notice_to_admin, text="notice_to_admin")
dp.register_callback_query_handler(edit_quiz_question, cb.filter())





async def main():

    # Регистрация хэндлеров
    # register(dp)

    # dp.register_message_handler(rrr, commands="rrrr")

    # Установка команд бота
    await set_commands(bot)



async def on_startup(dp):
    logging.warning('Starting connection')
    await bot.set_webhook(WEBHOOK_URL)
    # asyncio.create_task(bot_schedule())



async def on_shutdown(dp):
    logging.warning('Bye! Shutting down webhook connection')


if __name__ == '__main__':
    if USE_WEBHOOK:
        start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
                      on_startup=on_startup, on_shutdown=on_shutdown,
                      host=WEBAPP_HOST, port=WEBAPP_PORT, skip_updates=True)
        asyncio.run(main())
    else:
        executor.start_polling(dp, skip_updates=True)



