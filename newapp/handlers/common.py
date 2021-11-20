import logging
from random import randint
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.utils import exceptions
from aiogram.utils.exceptions import BotBlocked
from newapp.bt import bot
from newapp.config import test_group
from aiogram.utils.markdown import link


# @dp.message_handler(commands=['start'], state="*")
from newapp.loader import user_data


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(f"Hello {message.from_user.first_name}!\n"
                         "Ask me and I can ask the whole World!",
                         reply_markup=types.ReplyKeyboardRemove()
    )
    await ask_start(message)



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




async def close_session(call: types.CallbackQuery):
    await call.message.answer("It`s the close_session")
    await call.answer(text="Buy!", show_alert=True)
    # или просто await call.answer()


async def notice_to_admin(call: types.CallbackQuery):
    user_id = call.from_user.id
    user = user_data[user_id]

    try:
        # await call.answer("Is this a mistake????")
        await bot.send_message(test_group, f"A new message has been received with Session_id = {user.session_id}", disable_notification=False)
        # await bot.send_message(test_group, 'New question was recevied')
        # await bot.send_message(me, 'New question was recevied')
        await close_session(call)

    except exceptions.BotBlocked:
        logging.error(f"Target [ID:{test_group}]: blocked by user")
        await close_session(call)




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



async def testing(message: types.Message):
    # Handler for testing new features
    await message.answer(message.as_json())

async def testing2(message: types.Message):
    # Handler for testing new features
    updates = await bot.get_updates(offset=-1, timeout=1)
    await bot.send_message(test_group, len(updates))

    for update in updates:
        await bot.send_message(test_group, update)

    # updates = await bot.get_updates(offset=-1, timeout=1)
    # await bot.send_message(test_group, updates)

