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
    # Установка команд бота
    await set_commands(bot)




@dp.message_handler(commands=['start'], state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Hi my friend! \n"
                         "Ask me and I can ask the whole World!",
                         reply_markup=types.ReplyKeyboardRemove()
    )


@dp.message_handler(commands=['cancel', 'отмена'], state="*")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Action canceled", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['ask'], state="*")
async def ask_start(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="YES!", callback_data="start_session"),
        types.InlineKeyboardButton(text="NO :(", callback_data="close_session")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Are you ready?", reply_markup=keyboard)



@dp.callback_query_handler(text="start_session")
async def send_start_session(call: types.CallbackQuery):
    await call.message.answer("Send me your question")

    await call.answer(text="Thanks!", show_alert=True)
    # или просто await call.answer()


@dp.callback_query_handler(text="close_session")
async def send_close_session(call: types.CallbackQuery):
    await call.answer(text="Buy!", show_alert=True)
    # или просто await call.answer()




@dp.message_handler(commands="random")
async def cmd_random(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Press me", callback_data="random_value"))
    await message.answer("Number from 1 to 10", reply_markup=keyboard)


@dp.callback_query_handler(text="random_value")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer(str(randint(1, 10)))
    await call.answer(text="Thanks!", show_alert=True)
    # или просто await call.answer()



# обработчик исключения BotBlocked
@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    # Update: объект события от Telegram. Exception: объект исключения
    # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")

    # Такой хэндлер должен всегда возвращать True,
    # если дальнейшая обработка не требуется.
    return True





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


