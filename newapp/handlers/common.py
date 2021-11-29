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


async def cmd_start(message: types.Message):
    # await state.finish()

    buttons = [
        types.InlineKeyboardButton(text="\U00002618  Ask a question", callback_data="start_session"),
        types.InlineKeyboardButton(text="\U0001F3F5  See my last question", callback_data="close_session"),
        types.InlineKeyboardButton(text="\U0001F4D5  Description", callback_data="description"),
        types.InlineKeyboardButton(text="\U00002699 Settings", callback_data="close_session")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await message.answer(f"Hello {message.from_user.first_name}!\n"
                         "Ask me and I can ask the whole World!",
                         reply_markup=keyboard)



async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Action canceled", reply_markup=types.ReplyKeyboardRemove())


async def description(call: types.CallbackQuery):
    # await call.answer(text="\U0001F603 Buy!", show_alert=True)
    # или просто await call.answer()
    buttons = [
        types.InlineKeyboardButton(text="\U00002B05  Back", callback_data="switcher") ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await call.message.answer("\U0001F4E2 It`s the description", reply_markup=keyboard)

async def switcher(call: types.CallbackQuery):
    await cmd_start(call.message)


async def close_session(call: types.CallbackQuery):
    await call.message.answer("It`s the close_session")
    await call.answer(text="\U0001F603 Buy!", show_alert=True)
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
    await message.answer(f"message id: {message.message_id}")

    buttons = [
        types.InlineKeyboardButton(text="test EDIT callback :)", callback_data="test_edit_callback"),
        types.InlineKeyboardButton(text="test DELETE callback :)", callback_data="test_delete_callback")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Are you ready?", reply_markup=keyboard)


async def testing2(message: types.Message):
    # Handler for testing new features
    updates = await bot.get_updates(offset=-1, timeout=1)
    await bot.send_message(test_group, len(updates))

    for update in updates:
        await bot.send_message(test_group, update)

    # updates = await bot.get_updates(offset=-1, timeout=1)
    # await bot.send_message(test_group, updates)


async def test_edit_callback(call: types.CallbackQuery):
    # await call.message.answer("It`s test callback")

    # buttons = [
    #     types.InlineKeyboardButton(text="NEW test callback :)", callback_data="test_edit_callback")
    # ]
    # keyboard = types.InlineKeyboardMarkup(row_width=1)
    # keyboard.add(*buttons)

    buttons = [
        types.InlineKeyboardButton(text="test EDIT callback : )", callback_data="test_edit_callback"),
        types.InlineKeyboardButton(text="test DELETE callback : )", callback_data="test_delete_callback")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)


async def test_delete_callback(call: types.CallbackQuery):
    # await call.message.answer("It`s test callback")

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    # buttons = [
    #     types.InlineKeyboardButton(text="NEW test callback instead of deleted one:)", callback_data="test_delete_callback")
    # ]
    # keyboard = types.InlineKeyboardMarkup(row_width=1)
    # keyboard.add(*buttons)

    buttons = [
        types.InlineKeyboardButton(text="test EDIT callback  :)", callback_data="test_edit_callback"),
        types.InlineKeyboardButton(text="test DELETE callback  :)", callback_data="test_delete_callback")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)


    await call.message.answer("Are you ready?", reply_markup=keyboard)

