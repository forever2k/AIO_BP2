from typing import Union
from aiogram import Dispatcher, types, md
from aiogram.dispatcher import FSMContext
from newapp.bt import bot
from newapp.config import test_group
from newapp.handlers.get_data_from_database import get_data_for_user
from newapp.keyboards import main_menu_inline_keyboard
from newapp.text_module import selected_text


async def switcher_to_main_menu(message: Union[types.Message,
                                               types.CallbackQuery], lang,
                                state: FSMContext):
    await state.finish()
    text = await selected_text(lang)

    keyboard = await main_menu_inline_keyboard()

    if isinstance(message, types.CallbackQuery):
        message = message.message

    await bot.edit_message_text(f"{text['First'][0]} {message.chat.first_name}!\n"
                                f"{text['First'][1]}", chat_id=message.chat.id,
                                message_id=message.message_id,
                                reply_markup=keyboard)


async def switcher_get_data_for_user(call: types.CallbackQuery):
    user_id = call.from_user.id
    await get_data_for_user(call.message, user_id=user_id)