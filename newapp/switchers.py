from typing import Union
from aiogram import Dispatcher, types, md
from aiogram.dispatcher import FSMContext
from newapp.bt import bot
from newapp.config import test_group
from newapp.handlers.get_data_from_database import get_data_for_user
from newapp.keyboards import main_menu_inline_keyboard
from newapp.language_module import check_current_user_language
from newapp.text_module import selected_text


async def switcher_to_main_menu(message: Union[types.Message,
                                               types.CallbackQuery],
                                state: FSMContext):
    await state.finish()

    # if isinstance(message, types.CallbackQuery):
    #     await bot.send_message(test_group, 'types.CallbackQuery')
    #     call = message

    lang = await check_current_user_language(message)
    text = await selected_text(lang)

    # await bot.send_message(test_group, lang)

    keyboard = await main_menu_inline_keyboard(text)

    # if isinstance(message, types.CallbackQuery):
    #     message = message.message
    if isinstance(message, types.CallbackQuery):
        call = message
        message = call.message

    await bot.edit_message_text(f"{text['first'][0]}"
                                f" {message.chat.first_name}!\n"
                                f"{text['first'][1]}", chat_id=message.chat.id,
                                message_id=message.message_id,
                                reply_markup=keyboard)


async def switcher_get_data_for_user(call: types.CallbackQuery):
    user_id = call.from_user.id
    await get_data_for_user(call, user_id=user_id)