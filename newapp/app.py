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
from newapp.language_module import set_rus_language, set_eng_language
from newapp.switchers import switcher_to_main_menu, switcher_get_data_for_user
from quizer import my_poll, send_poll

logging.basicConfig(level=logging.DEBUG)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Start"),
        BotCommand(command="/cancel", description="Cancel")
    ]
    await bot.set_my_commands(commands)


async def set_comm2(message: types.Message):
    await set_commands(bot)
    await message.answer("commands set success!")

dp.register_message_handler(cmd_start, commands="start", state="*")
dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
dp.register_message_handler(get_question, state=GetData.waiting_for_get_question)
# dp.register_message_handler(ask_answer, state=GetData.waiting_for_ask_answer)
dp.register_message_handler(write_answer, state=GetData.waiting_for_write_answer)
dp.register_message_handler(get_quiz_from_database_by_session_id, state=GetDataFromDatabase.waiting_for_get_session_id)
dp.register_message_handler(send_correct_question, state=GetDataFromDatabase.waiting_for_correct_question)
dp.register_message_handler(send_correct_answer, state=GetDataFromDatabase.waiting_for_correct_answer)
dp.register_message_handler(ask_session_id, IDFilter(user_id=[me, olenka]),
                            commands="asksecret")
dp.register_message_handler(check_admin_data, IDFilter(user_id=[me, olenka]), commands="checkdata", state="*")
dp.register_message_handler(my_poll, IDFilter(user_id=[me, olenka]), commands="mypoll",
                            state="*")
dp.register_message_handler(set_comm2, IDFilter(user_id=[me, olenka]),commands=[
    "comm2"], state="*")
dp.register_message_handler(switcher_to_main_menu, lambda message: message.text=="\U00002618 Main Menu", state="*")
dp.register_message_handler(close_session, lambda message: message.text == "\U00002618 Cancel", state="*")

dp.register_errors_handler(error_bot_blocked, exception=BotBlocked)

dp.register_callback_query_handler(start_session, text="start_session")
dp.register_callback_query_handler(close_session, text="close_session")
dp.register_callback_query_handler(description, text="description")
dp.register_callback_query_handler(get_answer, cb_number_answer.filter())
dp.register_callback_query_handler(notice_to_admin, text="notice_to_admin")
dp.register_callback_query_handler(edit_quiz_question, cb.filter())
dp.register_callback_query_handler(send_poll, text="send_poll")
dp.register_callback_query_handler(switcher_to_main_menu, text="switcher_to_main_menu")
dp.register_callback_query_handler(switcher_get_data_for_user, text="switcher_get_data_for_user")
dp.register_callback_query_handler(settings, text="settings")
dp.register_callback_query_handler(set_rus_language, text="set_rus_language")
dp.register_callback_query_handler(set_eng_language, text="set_eng_language")
dp.register_callback_query_handler(thanks_to_user, text="thanks_to_user")

async def main():

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
        asyncio.run(main())



