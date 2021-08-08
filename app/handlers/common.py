from random import randint
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.utils.exceptions import BotBlocked
from bot import dp


# @dp.message_handler(commands=['start'], state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Hi my friend! \n"
                         "Ask me and I can ask the whole World!",
                         reply_markup=types.ReplyKeyboardRemove()
    )


async def bbb(message: types.Message):
    await message.answer("bbbbbbbbbbbbbbbbbbbb")


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Action canceled", reply_markup=types.ReplyKeyboardRemove())



async def ask_start(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="YES!", callback_data="start_session"),
        types.InlineKeyboardButton(text="NO :(", callback_data="close_session")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Are you ready?", reply_markup=keyboard)



async def send_start_session(call: types.CallbackQuery):
    await call.message.answer("Send me your question")
    await call.answer(text="Thanks!", show_alert=True)
    # или просто await call.answer()



async def send_close_session(call: types.CallbackQuery):
    await call.answer(text="Buy!", show_alert=True)
    # или просто await call.answer()



async def cmd_random(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Press me", callback_data="random_value"))
    await message.answer("Number from 1 to 10", reply_markup=keyboard)


async def send_random_value(call: types.CallbackQuery):
    await call.message.answer(str(randint(1, 10)))
    await call.answer(text="Thanks!", show_alert=True)
    # или просто await call.answer()



# обработчик исключения BotBlocked
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    # Update: объект события от Telegram. Exception: объект исключения
    # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")

    # Такой хэндлер должен всегда возвращать True,
    # если дальнейшая обработка не требуется.
    return True


# Просто функция, которая доступна только администратору,
# чей ID указан в файле конфигурации.
async def secret_command(message: types.Message):
    await message.answer("Поздравляю! Эта команда доступна только администратору бота.")


def register(dp):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(bbb, commands=['bbb'])
    # dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    # dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(ask_start, commands=["ask"], state="*")
    # dp.register_message_handler(send_start_session, commands="start_session", state="*")
    # dp.register_message_handler(send_close_session, commands="close_session", state="*")
    dp.register_message_handler(cmd_random, commands=["random"], state="*")
    # dp.register_message_handler(send_random_value, commands="random_value", state="*")
    # dp.register_errors_handler(error_bot_blocked, exception=BotBlocked)
    # dp.register_message_handler(secret_command, IDFilter(user_id=admin_id), commands="abracadabra")