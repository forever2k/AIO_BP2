import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import exceptions
from newapp.bt import bot
from newapp.config import dbase, test_group, me
from newapp.handlers.get_data_from_user import write_to_database
from newapp.loader import *


# available_questions = ["вопрос1", "вопрос3", "вопрос3"]
# available_answers = ["ответ1", "ответ2", "ответ3"]


cursor = dbase.cursor()

class GetDataFromDatabase(StatesGroup):
    waiting_for_get_session_id = State()
    waiting_for_correct_question = State()
    waiting_for_correct_answer = State()


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

    quiz = await get_data(message=message, session_id=session_id, whole_quiz='Yes')

    if len(quiz) > 0:
        await message.answer(f'User_id = {quiz["user_id"]} \n'
                             f'session_id = {quiz["session_id"]} \n'
                             f'Datetime = {quiz["Datetime"]} \n'
                             f'QUESTION = {quiz["QUESTION"]} \n'
                             f'ANSWER1 = {quiz["ANSWER1"]} \n'
                             f'ANSWER2 = {quiz["ANSWER2"]} \n'
                             f'ANSWER3 = {quiz["ANSWER3"]} \n'
                             f'ANSWER4 = {quiz["ANSWER4"]} \n')

        await state.finish()
        # await bot.send_message(test_group, f'HEREEEEEEEEEEEEEEEEE 2222222222222222 {session_id}')
        await ask_for_quiz(message, session_id, quiz)
    else:
        await message.answer(f'len(quiz) < 0 .. :(')
        await ask_session_id(message)



async def get_data(message: types.Message=None, call: types.CallbackQuery=None, session_id=None, whole_quiz=None, chosen_quiz=None, entity=None):

    if whole_quiz == 'Yes':
        data_by_session_id = "SELECT * FROM users WHERE session_id = %s"
        cursor.execute(data_by_session_id, (session_id,))

        quiz = {}

        for (user_id, QUESTION, ANSWER1, session_id, ANSWER2, ANSWER3, ANSWER4, Datetime) in cursor:
            quiz['user_id'] = user_id
            quiz['session_id'] = session_id
            quiz['Datetime'] = Datetime
            quiz['QUESTION'] = QUESTION
            quiz['ANSWER1'] = ANSWER1
            quiz['ANSWER2'] = ANSWER2
            quiz['ANSWER3'] = ANSWER3
            quiz['ANSWER4'] = ANSWER4

        admin_data["session_id"] = quiz[session_id]
        admin_data["question"] = quiz[QUESTION]
        admin_data["answer1"] = quiz[ANSWER1]
        admin_data["answer2"] = quiz[ANSWER2]
        admin_data["answer3"] = quiz[ANSWER3]
        admin_data["answer4"] = quiz[ANSWER4]


        return quiz

            # await message.answer(f'User_id = {user_id} \n'
            #                      f'session_id = {session_id} \n'
            #                      f'Datetime = {Datetime} \n'
            #                      f'QUESTION = {QUESTION} \n'
            #                      f'ANSWER1 = {ANSWER1} \n'
            #                      f'ANSWER2 = {ANSWER2} \n'
            #                      f'ANSWER3 = {ANSWER3} \n'
            #                      f'ANSWER4 = {ANSWER4}')
    elif chosen_quiz == 'Yes':
        data_by_session_id = "SELECT * FROM users WHERE session_id = %s"
        cursor.execute(data_by_session_id, (session_id,))

        await bot.send_message(test_group, f'HERE 333333333333333 {entity} AND {session_id}')

        for (user_id, QUESTION, ANSWER1, session_id, ANSWER2, ANSWER3, ANSWER4, Datetime) in cursor:
                if entity == 'QUESTION':
                    await bot.send_message(test_group, f'HERE 666666666666666 {QUESTION}')
                    return QUESTION
                elif entity == 'ANSWER1':
                    await bot.send_message(test_group, f'HERE 5555555 {ANSWER1}')
                    return ANSWER1
                elif entity == 'ANSWER2':
                    return ANSWER2
                elif entity == 'ANSWER3':
                    return ANSWER3
                elif entity == 'ANSWER4':
                    return ANSWER4



async def ask_for_quiz(message: types.Message, session_id, quiz):
    await bot.send_message(test_group, "here 111")
    await bot.send_message(test_group, quiz)
    buttons = [
        types.InlineKeyboardButton(text="Edit", callback_data=cb.new(session_id=session_id)),
        types.InlineKeyboardButton(text="Send poll", callback_data=cb2.new(session_id=session_id, quiz=quiz)),
        types.InlineKeyboardButton(text="Cancel", callback_data="close_session"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("What do you want to do with the Quiz?", reply_markup=keyboard)


async def edit_quiz_question(call: types.CallbackQuery, callback_data: dict, admin_data=admin_data):

    session_id = callback_data["session_id"]

    current_data = 'current_data'
    admin_data[current_data] = Admin()
    admin = admin_data[current_data]
    admin.session_id = session_id

    # await bot.send_message(test_group, f"current Session_id = {session_id}")
    question = await get_data(session_id=session_id, chosen_quiz='Yes', entity='QUESTION')

    await call.message.answer(f'Question for Session_id {session_id} was:')
    await call.message.answer(question)
    await call.message.answer(f'Please write correct Question for Session_id {session_id}')
    await GetDataFromDatabase.waiting_for_correct_question.set()



async def send_correct_question(message: types.Message, state: FSMContext, admin_data=admin_data):

    edit_question = message.text
    admin = admin_data['current_data']
    admin.question = edit_question
    session_id = admin.session_id

    await write_to_database(message, session_id, question=edit_question)

    await ask_correct_answers(message)



async def send_correct_answer(message: types.Message, state: FSMContext, admin_data=admin_data):

    edit_answer = message.text
    admin = admin_data['current_data']
    session_id = admin.session_id

    if admin.answer1 == '':
        admin.answer1 = edit_answer
        await write_to_database(message, session_id, answer1=admin.answer1)
        await ask_correct_answers(message)
    elif admin.answer2 == '':
        admin.answer2 = edit_answer
        await write_to_database(message, session_id, answer2=admin.answer2)
        await ask_correct_answers(message)
    elif admin.answer3 == '':
        admin.answer3 = edit_answer
        await write_to_database(message, session_id, answer3=admin.answer3)
        await ask_correct_answers(message)
    elif admin.answer4 == '':
        admin.answer4 = edit_answer
        await write_to_database(message, session_id, answer4=admin.answer4)
        await state.finish()




async def ask_correct_answers(message: types.Message, admin_data=admin_data):

    admin = admin_data['current_data']
    session_id = admin.session_id

    if admin.answer1 == '':
        entity = 'ANSWER1'
        await message.answer(f'{entity} for Session_id {session_id} was:')
        text_answer = await get_data(session_id=session_id, chosen_quiz='Yes', entity=entity)
        if text_answer == None:
            await message.answer(f'Answer for {entity} = NONE')
            await message.answer(f'Please write correct {entity} for Session_id {session_id}')
            await GetDataFromDatabase.waiting_for_correct_answer.set()
        else:
            await message.answer(text_answer)
            await message.answer(f'Please write correct {entity} for Session_id {session_id}')
            await GetDataFromDatabase.waiting_for_correct_answer.set()
    elif admin.answer2 == '':
        entity = 'ANSWER2'
        await message.answer(f'{entity} for Session_id {session_id} was:')
        text_answer = await get_data(session_id=session_id, chosen_quiz='Yes', entity=entity)
        if text_answer == None:
            await message.answer(f'Answer for {entity} = NONE')
            await message.answer(f'Please write correct {entity} for Session_id {session_id}')
            await GetDataFromDatabase.waiting_for_correct_answer.set()
        else:
            await message.answer(text_answer)
            await message.answer(f'Please write correct {entity} for Session_id {session_id}')
            await GetDataFromDatabase.waiting_for_correct_answer.set()
    elif admin.answer3 == '':
        entity = 'ANSWER3'
        await message.answer(f'{entity} for Session_id {session_id} was:')
        text_answer = await get_data(session_id=session_id, chosen_quiz='Yes', entity=entity)
        if text_answer == None:
            await message.answer(f'Answer for {entity} = NONE')
            await message.answer(f'Please write correct {entity} for Session_id {session_id}')
            await GetDataFromDatabase.waiting_for_correct_answer.set()
        else:
            await message.answer(text_answer)
            await message.answer(f'Please write correct {entity} for Session_id {session_id}')
            await GetDataFromDatabase.waiting_for_correct_answer.set()
    elif admin.answer4 == '':
        entity = 'ANSWER4'
        await message.answer(f'{entity} for Session_id {session_id} was:')
        text_answer = await get_data(session_id=session_id, chosen_quiz='Yes', entity=entity)
        if text_answer == None:
            await message.answer(f'Answer for {entity} = NONE')
            await message.answer(f'Please write correct {entity} for Session_id {session_id}')
            await GetDataFromDatabase.waiting_for_correct_answer.set()
        else:
            await message.answer(text_answer)
            await message.answer(f'Please write correct {entity} for Session_id {session_id}')



async def check_admin_data(message: types.Message, admin_data=admin_data):
    await message.answer(len(admin_data))