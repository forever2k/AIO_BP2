import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import exceptions
from newapp.bt import bot
from newapp.config import dbase, test_group
from newapp.handlers.get_data_from_user import write_to_database
from newapp.language_module import check_current_user_language
from newapp.loader import *
from newapp.keyboards import main_menu_inline_keyboard, send_poll_menu
from newapp.text_module import selected_text

cursor = dbase.cursor()

class GetDataFromDatabase(StatesGroup):
    waiting_for_get_session_id = State()
    waiting_for_correct_question = State()
    waiting_for_correct_answer = State()


async def ask_session_id(message: types.Message):
    await message.answer("Please write number of Session_id to get data from database")

    await GetDataFromDatabase.waiting_for_get_session_id.set()


async def get_quiz_from_database_by_session_id(message: types.Message, state: FSMContext):

    session_id = message.text

    try:
        quiz = await get_data_for_admin(message=message, session_id=session_id, whole_quiz='Yes')
    except Exception as e:
        await message.answer('You sent the wrong session_id. Please try again')
        return

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
        await ask_for_quiz(message, session_id)
    else:
        await message.answer(f'len(quiz) < 0 .. :(')
        await ask_session_id(message)


async def get_data_for_admin(message: types.Message=None, call: types.CallbackQuery=None, session_id=None, whole_quiz=None, chosen_quiz=None, entity=None, admin_data=admin_data):

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

        admin_data["session_id"] = quiz['session_id']
        admin_data["question"] = quiz['QUESTION']
        admin_data["answer1"] = quiz['ANSWER1']
        admin_data["answer2"] = quiz['ANSWER2']
        admin_data["answer3"] = quiz['ANSWER3']
        admin_data["answer4"] = quiz['ANSWER4']

        return quiz

    elif chosen_quiz == 'Yes':
        data_by_session_id = "SELECT * FROM users WHERE session_id = %s"
        cursor.execute(data_by_session_id, (session_id,))

        for (user_id, QUESTION, ANSWER1, session_id, ANSWER2, ANSWER3, ANSWER4, Datetime) in cursor:
                if entity == 'QUESTION':
                    return QUESTION
                elif entity == 'ANSWER1':
                    return ANSWER1
                elif entity == 'ANSWER2':
                    return ANSWER2
                elif entity == 'ANSWER3':
                    return ANSWER3
                elif entity == 'ANSWER4':
                    return ANSWER4


async def ask_for_quiz(message: types.Message, session_id):

    keyboard = await send_poll_menu(session_id)
    await message.answer("What do you want to do with the Quiz?", reply_markup=keyboard)


async def edit_quiz_question(call: types.CallbackQuery, callback_data: dict, admin_data=admin_data):

    session_id = callback_data["session_id"]

    current_data = 'current_data'
    admin_data[current_data] = Admin()
    admin = admin_data[current_data]
    admin.session_id = session_id

    question = await get_data_for_admin(session_id=session_id, chosen_quiz='Yes', entity='QUESTION')

    await call.message.answer(f'Question for Session_id {session_id} was:')
    await call.message.answer(question)
    await call.message.answer(f'Please write correct Question for Session_id {session_id}')
    await GetDataFromDatabase.waiting_for_correct_question.set()


async def send_correct_question(message: types.Message, state: FSMContext, admin_data=admin_data):

    await message.answer('HERE 777777777777777 !! !')

    edit_question = message.text
    admin = admin_data['current_data']
    admin.question = edit_question
    session_id = admin.session_id

    await write_to_database(message, session_id, question=edit_question)

    await ask_correct_answers(message)


async def send_correct_answer(message: types.Message, state: FSMContext, admin_data=admin_data):

    await message.answer('HERE 555555555555 !!!!!!!!!!!!!!!!1')

    edit_answer = message.text
    admin = admin_data['current_data']
    session_id = admin.session_id

    await message.answer('HERE 55555555555566666666666 !!!!!!!!!!!!!!!!1')

    if admin.answer1 == '':
        admin.answer1 = edit_answer
        await write_to_database(message, session_id, answer1=admin.answer1)
        await state.finish()
        await ask_correct_answers(message)
    elif admin.answer2 == '':
        admin.answer2 = edit_answer
        await write_to_database(message, session_id, answer2=admin.answer2)
        await state.finish()
        await ask_correct_answers(message)
    elif admin.answer3 == '':
        admin.answer3 = edit_answer
        if admin.answer3.lower() == 'none':
            await write_to_database(message, session_id, answer3=None)
            await state.finish()
        else:
            await write_to_database(message, session_id, answer3=admin.answer3)
            await state.finish()
            await ask_correct_answers(message)
    elif admin.answer4 == '':
        await message.answer('HERE 333333333333!!!!!!!!!!!!!!!!!!!')
        admin.answer4 = edit_answer
        if admin.answer4.lower() == 'none':
            await write_to_database(message, session_id, answer4=None)
            await state.finish()
            await message.answer('Done!')
        else:
            await write_to_database(message, session_id, answer4=admin.answer4)
            await state.finish()
            await message.answer('Done!')


async def ask_correct_answers(message: types.Message, admin_data=admin_data):

    admin = admin_data['current_data']
    session_id = admin.session_id

    if admin.answer1 == '':
        entity = 'ANSWER1'
        await message.answer(f'{entity} for Session_id {session_id} was:')
        text_answer = await get_data_for_admin(session_id=session_id, chosen_quiz='Yes', entity=entity)
        if text_answer == None:
            await message.answer(f'Answer for {entity} = NONE')
        else:
            await message.answer(text_answer)
    elif admin.answer2 == '':
        entity = 'ANSWER2'
        await message.answer(f'{entity} for Session_id {session_id} was:')
        text_answer = await get_data_for_admin(session_id=session_id, chosen_quiz='Yes', entity=entity)
        if text_answer == None:
            await message.answer(f'Answer for {entity} = NONE')
        else:
            await message.answer(text_answer)
    elif admin.answer3 == '':
        entity = 'ANSWER3'
        await message.answer(f'{entity} for Session_id {session_id} was:')
        text_answer = await get_data_for_admin(session_id=session_id, chosen_quiz='Yes', entity=entity)
        if text_answer == None:
            await message.answer(f'Answer for {entity} = NONE')
        else:
            await message.answer(text_answer)
    elif admin.answer4 == '':
        entity = 'ANSWER4'
        await message.answer(f'{entity} for Session_id {session_id} was:')
        text_answer = await get_data_for_admin(session_id=session_id, chosen_quiz='Yes', entity=entity)
        if text_answer == None:
            await message.answer(f'Answer for {entity} = NONE')
        else:
            await message.answer(text_answer)

    await message.answer(f'Please write correct {entity} for Session_id {session_id} or write "none" if you don`t send {entity} ')
    await GetDataFromDatabase.waiting_for_correct_answer.set()


async def check_admin_data(message: types.Message, admin_data=admin_data):
    await message.answer(len(admin_data))


async def get_last_user_session_id(message: types.Message):
    user_id = message.from_user.id


async def get_data_for_user(message, user_id=None,
                            session_id=None):

    lang = await check_current_user_language(message)
    text = await selected_text(lang)

    keyboard = await main_menu_inline_keyboard(text)

    if isinstance(message, types.CallbackQuery):
        message = message.message

    if session_id == None:
        last_data_by_user_id = "SELECT * FROM users WHERE user_id = %s order by Datetime desc limit 1"
        cursor.execute(last_data_by_user_id, (user_id,))
        quiz = cursor.fetchone()

        date = quiz[7].date()
        time = quiz[7].time()

        answer3 = quiz[5] if quiz[5] != None else '-'
        answer4 = quiz[6] if quiz[6] != None else '-'

        await bot.delete_message(chat_id= message.chat.id,
                                 message_id=message.message_id)

        await message.answer(f'{text["last_quize"][0]}  \n' 
                             f'{text["last_quize"][1]} {date} {time} \n' 
                             f'{text["last_quize"][2]} {quiz[1]} \n'
                             f'{text["last_quize"][3]} {quiz[2]} \n'
                             f'{text["last_quize"][4]} {quiz[4]} \n'
                             f'{text["last_quize"][5]} {answer3} \n'
                             f'{text["last_quize"][6]} {answer4} \n\n'
                             f'{text["last_quize"][7]}', reply_markup=keyboard)
