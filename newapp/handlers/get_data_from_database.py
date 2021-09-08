import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import exceptions
from newapp.bt import bot
from newapp.config import dbase, test_group, me
from newapp.loader import *

# available_questions = ["вопрос1", "вопрос3", "вопрос3"]
# available_answers = ["ответ1", "ответ2", "ответ3"]


cursor = dbase.cursor()

class GetDataFromDatabase(StatesGroup):
    waiting_for_get_session_id = State()
    waiting_for_correct_question = State()


async def ask_session_id(message: types.Message):
    await message.answer("Please write number of Session_id to get data from database")
    await GetDataFromDatabase.waiting_for_get_session_id.set()


async def get_quiz_from_database(message: types.Message, state: FSMContext):
    session_id = message.text
    # await bot.send_message(test_group, message.text)

    # data_by_session_id = "SELECT * FROM users WHERE session_id = %s"
    # cursor.execute(data_by_session_id, (session_id,))
    #
    # for (user_id, QUESTION, ANSWER1, session_id, ANSWER2, ANSWER3, ANSWER4, Datetime) in cursor:
    #     await message.answer(f'User_id = {user_id},\n'
    #                          f'session_id = {session_id},\n'
    #                          f'Datetime = {Datetime},\n'
    #                          f'QUESTION = {QUESTION},\n'
    #                          f'ANSWER1 = {ANSWER1},\n'
    #                          f'ANSWER2 = {ANSWER2},\n'
    #                          f'ANSWER3 = {ANSWER3},\n'
    #                          f'ANSWER4 = {ANSWER4}')

    # data_by_session_id = "SELECT * FROM users WHERE session_id = %s"
    # cursor.execute(data_by_session_id, (session_id,))
    #
    # for (user_id, QUESTION) in cursor:
    #     await message.answer(f"User_id = {user_id}, QUESTION = {QUESTION}")

    await get_data(message=message, session_id=session_id, whole_quiz='Yes')
    await state.finish()
    await ask_edit_quiz(message, session_id)


async def get_data(message: types.Message=None, call: types.CallbackQuery=None, session_id=None, whole_quiz=None, chosen_quiz=None, entity=None):

    if whole_quiz == 'Yes':
        data_by_session_id = "SELECT * FROM users WHERE session_id = %s"
        cursor.execute(data_by_session_id, (session_id,))

        for (user_id, QUESTION, ANSWER1, session_id, ANSWER2, ANSWER3, ANSWER4, Datetime) in cursor:
            await message.answer(f'User_id = {user_id} \n'
                                 f'session_id = {session_id} \n'
                                 f'Datetime = {Datetime} \n'
                                 f'QUESTION = {QUESTION} \n'
                                 f'ANSWER1 = {ANSWER1} \n'
                                 f'ANSWER2 = {ANSWER2} \n'
                                 f'ANSWER3 = {ANSWER3} \n'
                                 f'ANSWER4 = {ANSWER4}')
    elif chosen_quiz == 'Yes':
        data_by_session_id = "SELECT * FROM users WHERE session_id = %s"
        cursor.execute(data_by_session_id, (session_id,))

        for (user_id, QUESTION, ANSWER1, session_id, ANSWER2, ANSWER3, ANSWER4, Datetime) in cursor:
            if entity == 'QUESTION':
                return QUESTION
            elif entity == 'ANSWER1':
                await call.message.answer(ANSWER1)
            elif entity == 'ANSWER2':
                await call.message.answer(ANSWER2)
            elif entity == 'ANSWER3':
                await call.message.answer(ANSWER3)
            elif entity == 'ANSWER4':
                await call.message.answer(ANSWER4)



async def ask_edit_quiz(message: types.Message, session_id):
    buttons = [
        types.InlineKeyboardButton(text="YES", callback_data=cb.new(session_id=session_id)),
        types.InlineKeyboardButton(text="NO", callback_data="close_session"),
        types.InlineKeyboardButton(text="Cancel", callback_data="close_session"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Do you want to edit the Quiz?", reply_markup=keyboard)


async def edit_quiz_question(call: types.CallbackQuery, callback_data: dict):
    session_id = callback_data["session_id"]
    # await bot.send_message(test_group, f"current Session_id = {session_id}")
    question = await get_data(call=call, session_id=session_id, chosen_quiz='Yes', entity='QUESTION')
    await call.message.answer(f'Question for Session_id {session_id} was:')
    await call.message.answer(question)
    await call.message.answer(f'Please write correct Question for Session_id {session_id}')
    await GetDataFromDatabase.waiting_for_correct_question.set()

