import asyncio
import logging
from random import randint
from typing import Union
from aiogram import Dispatcher, types, md
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.utils import exceptions
from aiogram.utils.exceptions import BotBlocked
from newapp.bt import bot
from newapp.config import test_group
import json
from aiogram.utils.markdown import link
from newapp.handlers.get_data_from_database import get_data_for_user
from newapp.keyboards import main_menu_inline_keyboard, description_menu, settings_menu
from newapp.language_module import set_default_language
from newapp.loader import user_data


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()

    keyboard = await main_menu_inline_keyboard()
    await message.answer(f"Hello {message.chat.first_name}!\n"
                         "Ask me and I can ask the whole World!",
                         reply_markup=keyboard)

    await set_default_language(message)


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Action canceled", reply_markup=types.ReplyKeyboardRemove())


async def description(call: types.CallbackQuery):
    keyboard = await description_menu()
    await bot.edit_message_text("\U0001F4E2 It`s the description", chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        reply_markup=keyboard)

    # await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
    #                                     reply_markup=keyboard)
    #
    # await call.message.answer("\U0001F4E2 It`s the description", reply_markup=keyboard)


async def settings(call: types.CallbackQuery):
    keyboard = await settings_menu()
    await bot.edit_message_text("\U0001F4E2 Choose language", chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        reply_markup=keyboard)

# async def set_russian(call: types.CallbackQuery):
#
#     data_by_session_id = "SELECT * FROM users WHERE session_id = %s"
#     cursor.execute(data_by_session_id, (session_id,))


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




# async def cmd_random(message: types.Message):
#     keyboard = types.InlineKeyboardMarkup()
#     keyboard.add(types.InlineKeyboardButton(text="Press me", callback_data="random_value"))
#     await message.answer("Number from 1 to 10", reply_markup=keyboard)


# async def send_random_value(call: types.CallbackQuery):
#     await call.message.answer(str(randint(1, 10)))
#     await call.answer(text="Thanks!", show_alert=True)
#     # или просто await call.answer()



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

async def testing_edit_message(message: types.Message):
    await message.answer(message.message_id)

    await message.answer("hello")
    await asyncio.sleep(1)
    message2 = await bot.send_message(message.chat.id, 'Test!')
    await message.answer(message2.message_id)


    # await bot.send_message(message.chat.id, message.message_id)

    await asyncio.sleep(1)



    # final = json.loads(tt.text)
    # await message.answer(final)
    #
    # Dict = final['result']
    #
    # for obj in Dict:
    #     await message.answer(obj['update_id'])
    #     await message.answer(obj['message']['text'])

    #
    # await bot.edit_message_text('This is edited message', chat_id=message.chat.id,
    #                             message_id=edit)


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



#
#
# async def cmd_start(message: Union[types.Message, types.CallbackQuery], state: FSMContext):
#     await state.finish()
#
#     keyboard = await main_menu_keyboard()
#
#     if isinstance(message, types.Message):
#         await message.answer(f"Hello {message.chat.first_name}!\n"
#                              "Ask me and I can ask the whole World!",
#                              reply_markup=keyboard)
#
#     if isinstance(message, types.CallbackQuery):
#         call=message
#         await call.message.answer(f"Hello {call.message.chat.first_name}!\n"
#                              "Ask me and I can ask the whole World!",
#                              reply_markup=keyboard)