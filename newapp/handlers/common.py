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
from newapp.keyboards import main_menu_inline_keyboard, description_menu, settings_menu
from newapp.language_module import check_current_user_language
from newapp.loader import user_data, user_data_settings
from newapp.text_module import selected_text


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()

    lang = await check_current_user_language(message)
    text = await selected_text(lang)

    # await bot.send_message(test_group, lang)

    keyboard = await main_menu_inline_keyboard(text)

    await message.answer(f"{text['first'][0]} {message.chat.first_name}!\n"
                         f"{text['first'][1]}",
                         reply_markup=keyboard)

    # await set_default_language(message)


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await close_session(message)
    # await message.answer("Action canceled", reply_markup=types.ReplyKeyboardRemove())


async def description(call: types.CallbackQuery):

    lang = await check_current_user_language(call)
    text = await selected_text(lang)
    keyboard = await description_menu(text)

    await bot.edit_message_text(text["description_menu"][1],
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                        reply_markup=keyboard)

    # await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
    #                                     reply_markup=keyboard)
    #
    # await call.message.answer("\U0001F4E2 It`s the description", reply_markup=keyboard)


async def settings(call: types.CallbackQuery):

    lang = await check_current_user_language(call)
    text = await selected_text(lang)

    keyboard = await settings_menu(text)
    await bot.edit_message_text(text['settings_menu'][0],
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                        reply_markup=keyboard)

# async def set_russian(call: types.CallbackQuery):
#
#     data_by_session_id = "SELECT * FROM users WHERE session_id = %s"
#     cursor.execute(data_by_session_id, (session_id,))


async def close_session(message: Union[types.Message, types.CallbackQuery]):

    lang = await check_current_user_language(message)
    text = await selected_text(lang)

    if isinstance(message, types.CallbackQuery):
        call = message
        message = message.message

    await bot.delete_message(chat_id=message.chat.id,
                             message_id=message.message_id)

    await message.answer(text["close_session"][0], reply_markup=types.ReplyKeyboardRemove())

    try:
        await call.answer(text=text["close_session"][1], show_alert=True)
    except:
        pass


async def thanks_to_user(message: Union[types.Message, types.CallbackQuery]):
    lang = await check_current_user_language(message)
    text = await selected_text(lang)

    await notice_to_admin(message)

    if isinstance(message, types.CallbackQuery):
        call = message
        message = call.message

        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=message.message_id)

    await message.answer(text["ask_world"][16])



async def notice_to_admin(message: types.Message):

    user_id = message.from_user.id
    user = user_data[user_id]

    try:
        await bot.send_message(-1001153348142, f"A new message has been received "
                                           f"with Session_id:", disable_notification=False)
        await bot.send_message(test_group, user.session_id,
                               disable_notification=False)

    except exceptions.BotBlocked:
        logging.error(f"Target [ID:{test_group}]: blocked by user")


async def error_bot_blocked(update: types.Update, exception: BotBlocked):

    await bot.send_message(test_group, f"I was blocked by a user!\nMessage: {update}\nError:"
          f" {exception}")

    return True
