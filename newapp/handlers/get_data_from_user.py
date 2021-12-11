import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import exceptions
from newapp.bt import bot
from newapp.config import dbase, test_group, me
from newapp.loader import *
import time
from typing import Union

# available_questions = ["вопрос1", "вопрос3", "вопрос3"]
# available_answers = ["ответ1", "ответ2", "ответ3"]


cursor = dbase.cursor()

class GetData(StatesGroup):
    waiting_for_get_question = State()
    # waiting_for_ask_answer = State()
    waiting_for_write_answer = State()



async def start_session(call: types.CallbackQuery):
    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # for name in available_questions:
    #     keyboard.add(name)
    # await call.message.answer("Send me your question:", reply_markup=keyboard)

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


    # await bot.edit_message_text("Send me your question here:", chat_id=call.message.chat.id,
    #                             message_id=call.message.message_id, reply_markup=keyboard)

    await call.message.answer("Send me your question here:")
    await GetData.waiting_for_get_question.set()
    # await call.answer(text="Thanks!", show_alert=True)
    # или просто await call.answer()


async def get_question(message: types.Message, state: FSMContext, user_data=user_data):
    if len(message.text) < 5:
        await message.answer("You wrote a very short answer. Please try again.")
        return
    elif len(message.text) > 500:
        await message.answer("You wrote a very big answer. Please try again.")
        return
    else:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)
        user = user_data[user_id]
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
        await message.answer("You need to write from 2 to 4 answers\n"
                             "Now write and send your First Answer:")
        await ask_answer(message)


async def keyboard_answer(message: types.Message, number_answer):
    buttons = [
        types.InlineKeyboardButton(text="Yes", callback_data="get_answer"),
        types.InlineKeyboardButton(text="No", callback_data="notice_to_admin")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    await message.answer(f"Do you want to write your {number_answer} answer?", reply_markup=keyboard)




async def ask_answer(message: types.Message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        if user.answer1 == '':
            await get_answer(message, edit_indication='no')
        elif user.answer2 == '':
            await message.answer("Now write and send your Second Answer:")
            await get_answer(message, edit_indication='no')
        elif user.answer3 == '':
            await keyboard_answer(message, "Third")
        elif user.answer4 == '':
            await keyboard_answer(message, "Fourth")

        # if user.answer1 == '' or user.answer2 == '' or user.answer3 == '' or user.answer4 == '':
        #     buttons = [
        #         types.InlineKeyboardButton(text="Yes", callback_data="get_answer"),
        #         types.InlineKeyboardButton(text="No", callback_data="notice_to_admin")
        #     ]
        #     keyboard = types.InlineKeyboardMarkup(row_width=3)
        #     keyboard.add(*buttons)
        #     await message.answer("Do you want to write your answer?", reply_markup=keyboard)
        else:
            await message.answer("Thanks! Your answers are recorded")

    except Exception as e:
        await message.answer("[ask_answer] Something went wrong.. Please contact the admin")




async def get_answer(message: Union[types.Message, types.CallbackQuery], edit_indication=None):

    if isinstance(message, types.CallbackQuery):
        message = message.message
    # await call.message.answer("Now write your ANSWER")

    if edit_indication=='no':
        pass
    else:
        await bot.edit_message_text("Now write your next ANSWER:", chat_id=message.chat.id,
                                    message_id=message.message_id)

    await GetData.waiting_for_write_answer.set()


async def write_answer(message: types.Message, state: FSMContext):
    if len(message.text) < 2:
        await message.answer("You wrote a very short answer. Please try again.")
        return
    elif len(message.text) > 100:
        await message.answer("You wrote a very big answer. Please try again.")
        return
    # await state.update_data(chosen_answer=message.text.lower())
    # user_data = await state.get_data()

    try:
        user_id = message.from_user.id
        user = user_data[user_id]

        # try:
        #     sql = "INSERT INTO users (session_id, user_id, QUESTION, ANSWER1) \
        #                                                       VALUES (%s, %s, %s, %s)"
        #     val = (session_id, user_id, user.question, user.answer1)
        #     cursor.execute(sql, val)
        #     dbase.commit()
        #
        # except Exception as e:
        #     await message.reply(message, 'Something went wrong.. Please contact the admin')

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
        await message.answer("[write_answer] Something went wrong.. Please contact the admin")

    # try:
    #     await message.answer("Is this a mistake????")
    #     await bot.send_message(test_group, "A new message has been received", disable_notification=False)
    #     # await bot.send_message(test_group, 'New question was recevied')
    #     # await bot.send_message(me, 'New question was recevied')
    #
    # except exceptions.BotBlocked:
    #     logging.error(f"Target [ID:{test_group}]: blocked by user")

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
            await message.answer("Something went wrong.. Please contact the admin")
            # await message.reply(message, 'Something went wrong.. Please contact the admin')

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
            await message.answer("[write_to_database] Something went wrong.. Please contact the admin")
            # await message.reply(message, 'Something went wrong.. Please contact the admin')


        # await message.answer("check_session_query_val != 0 ! ! ! ")
        # await message.reply(message, 'check_session_query_val != 0 ! ! ! ')



# async def get_question(message: types.Message, state: FSMContext):
#     if len(message.text) < 5:
#         await message.answer("Пожалуйста, напишите корректный вопрос, используя клавиатуру ниже.")
#         return
#     await state.update_data(chosen_question=message.text.lower())
#
#     # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     # for size in available_answers:
#     #     keyboard.add(size)
#     await GetData.waiting_for_answer.set()
#     # await message.answer("Now write your ANSWER", reply_markup=keyboard)
#     await message.answer("Now write your ANSWER (from 2 to 4 answers)")
#
#
#
# async def get_answer(message: types.Message, state: FSMContext):
#     user_data = await state.get_data()
#     if len(message.text) < 5:
#         await message.answer("Пожалуйста, напишите вопрос, используя клавиатуру ниже.")
#         return
#     await state.update_data(chosen_answer=message.text.lower())
#     user_data = await state.get_data()
#     await message.answer(f"Length of user_data = {len(user_data)}")
#     await message.answer(f"Вы написали вопрос: {user_data['chosen_question']}.\n"
#                          f"Вы написали ответ: {user_data['chosen_answer']}.\n"
#                          f"Попробуйте теперь задать еще вопрос: /start", reply_markup=types.ReplyKeyboardRemove())
#
#     user_id = message.from_user.id
#     bd_id = generate_number(user_id)
#

#     try:
#
#         sql = "INSERT INTO users (bd_id, user_id, QUESTION, ANSWER) \
#                                                           VALUES (%s, %s, %s, %s)"
#         val = (bd_id, user_id, user_data['chosen_question'], user_data['chosen_answer'])
#         cursor.execute(sql, val)
#         dbase.commit()
#
#     except Exception as e:
#         await message.reply(message, 'Something went wrong.. Please contact the admin')
#
#     try:
#         await message.answer("it`s the last part")
#         await bot.send_message(test_group, "A new message has been received", disable_notification=False)
#         # await bot.send_message(test_group, 'New question was recevied')
#         # await bot.send_message(me, 'New question was recevied')
#
#     except exceptions.BotBlocked:
#         logging.error(f"Target [ID:{test_group}]: blocked by user")
#
#     await state.finish()
