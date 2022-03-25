import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import exceptions
from newapp.bt import bot
from newapp.config import dbase, test_group, me
from newapp.handlers.common import thanks_to_user
from newapp.keyboards import ask_for_answer_menu
from newapp.language_module import check_current_user_language
from newapp.loader import *
import time
from typing import Union
from newapp.text_module import selected_text

cursor = dbase.cursor()

class GetData(StatesGroup):
    waiting_for_get_question = State()
    waiting_for_write_answer = State()



async def start_session(call: types.CallbackQuery):

    lang = await check_current_user_language(call)
    text = await selected_text(lang)

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    await call.message.answer(text["ask_world"][0])
    await GetData.waiting_for_get_question.set()


async def get_question(message: types.Message, state: FSMContext, user_data=user_data):
    lang = await check_current_user_language(message)
    text = await selected_text(lang)

    if len(message.text) < 5:
        await message.answer(text["ask_world"][1])
        return
    elif len(message.text) > 500:
        await message.answer(text["ask_world"][2])
        return
    else:
        user_id = message.from_user.id
        user_data[user_id] = User()
        user = user_data[user_id]
        user.question = message.text
        session_id = generate_number(user_id)
        user.session_id = session_id

        await write_to_database(message, user.session_id, user_id, question=user.question)

        await state.finish()

    # await state.update_data(chosen_question=message.text.lower())
    # user_data = await state.get_data()


    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # for size in available_answers:
    #     keyboard.add(size)
    # await GetData.waiting_for_write_answer.set()
    # await message.answer("Now write your ANSWER", reply_markup=keyboard)
        await message.answer(f'{text["ask_world"][5]}'
                             f'{text["ask_world"][6]}')
        await ask_answer(message)


async def ask_for_answer(message: types.Message, number_answer):
    lang = await check_current_user_language(message)
    text = await selected_text(lang)
    keyboard = await ask_for_answer_menu(text, number_answer)
    await message.answer(f'{text["ask_world"][10]} {number_answer} '
                         f'{text["ask_world"][11]}',
                         reply_markup=keyboard)


async def ask_answer(message: types.Message):
    lang = await check_current_user_language(message)
    text = await selected_text(lang)

    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        if user.answer1 == '':
            await get_answer(message, edit_indication='no')
        elif user.answer2 == '':
            await message.answer(text["ask_world"][7])
            await get_answer(message, edit_indication='no')
        elif user.answer3 == '':
            number_answer = text["ask_world"][12]
            await ask_for_answer(message, number_answer)
        elif user.answer4 == '':
            number_answer = text["ask_world"][13]
            await ask_for_answer(message, number_answer)

        else:
            await thanks_to_user(message)

    except Exception as e:
        await bot.send_message(test_group,
                               f"There is a mistake in modul - 'ask_answer':"
                               f" {e}")
        await message.answer("Something went wrong.. Please contact the admin")


async def get_answer(message: Union[types.Message, types.CallbackQuery],
                     callback_data: dict = None, edit_indication=None):

    lang = await check_current_user_language(message)
    text = await selected_text(lang)

    if isinstance(message, types.CallbackQuery):
        message = message.message

    if edit_indication=='no':
        pass
    else:

        try:
            number_answer = callback_data["number_answer"]
        except Exception as e:
            await bot.send_message(test_group, "[get_answer] Something went "
                                               "wrong.. Please "
                                               "contact the admin")

        await bot.edit_message_text(f'{text["ask_world"][14]} {number_answer} {text["ask_world"][15]}',
                                    chat_id=message.chat.id,
                                    message_id=message.message_id)

    await GetData.waiting_for_write_answer.set()


async def write_answer(message: types.Message, state: FSMContext):
    lang = await check_current_user_language(message)
    text = await selected_text(lang)

    if len(message.text) < 2:
        await message.answer(text["ask_world"][3])
        return
    elif len(message.text) > 100:
        await message.answer(text["ask_world"][4])
        return

    try:
        user_id = message.from_user.id
        user = user_data[user_id]

        if user.answer1 =='':
            user.answer1 = message.text
            await write_to_database(message, user.session_id, user_id, answer1=user.answer1)
        elif user.answer2 =='':
            user.answer2 = message.text
            await write_to_database(message, user.session_id, user_id, answer2=user.answer2)
        elif user.answer3 == '':
            user.answer3 = message.text
            await write_to_database(message, user.session_id, user_id, answer3=user.answer3)
        elif user.answer4 == '':
            user.answer4 = message.text
            await write_to_database(message, user.session_id, user_id, answer4=user.answer4)

    except Exception as e:
        await bot.send_message(test_group,
                               f"There is a mistake in module - 'write_answer':"
                               f" {e}")
        await message.answer("Something went wrong.. Please contact the admin")

    await state.finish()
    await ask_answer(message)


async def write_to_database(message: types.Message, session_id, user_id=None, **kwargs):

    for key, val in kwargs.items():
        if key == 'question':
            answer_number = key
            question = val
        else:
            answer_number = key
            answer_text = val

    check_session_query = "SELECT * FROM users WHERE session_id = %s"
    cursor.execute(check_session_query, (session_id,))
    cursor.fetchall()

    if cursor.rowcount == 0:
        try:
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            insert_data_query = "INSERT INTO users (session_id, user_id, QUESTION, Datetime) \
                                                              VALUES (%s, %s, %s, %s)"
            val = (session_id, user_id, question, now)
            cursor.execute(insert_data_query, val)
            dbase.commit()

        except Exception as e:
            await bot.send_message(test_group,
                                   f"There is a mistake in modul - 'ask_answer':"
                                   f" {e}")
            await message.answer("Something went wrong.. Please contact the admin")

    else:
        try:
            if answer_number == 'question':
                update_data_query = "UPDATE users SET QUESTION = %s WHERE session_id = %s"
                val = (question, session_id)
                cursor.execute(update_data_query, val)
                dbase.commit()
            elif answer_number == 'answer1':
                update_data_query = "UPDATE users SET ANSWER1 = %s WHERE session_id = %s"
                val = (answer_text, session_id)
                cursor.execute(update_data_query, val)
                dbase.commit()

            elif answer_number == 'answer2':
                update_data_query = "UPDATE users SET ANSWER2 = %s WHERE session_id = %s"
                val = (answer_text, session_id)
                cursor.execute(update_data_query, val)
                dbase.commit()

            elif answer_number == 'answer3':
                update_data_query = "UPDATE users SET ANSWER3 = %s WHERE session_id = %s"
                val = (answer_text, session_id)
                cursor.execute(update_data_query, val)
                dbase.commit()

            elif answer_number == 'answer4':
                update_data_query = "UPDATE users SET ANSWER4 = %s WHERE session_id = %s"
                val = (answer_text, session_id)
                cursor.execute(update_data_query, val)
                dbase.commit()

        except Exception as e:
            await bot.send_message(test_group,
                                   f"There is a mistake in modul - 'write_to_database':"
                                   f" {e}")

            await message.answer("Something went wrong.. Please contact the admin")
