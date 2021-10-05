import logging
from aiogram import types
from newapp.bt import bot
from config import test_group
from newapp.handlers.get_data_from_database import ask_session_id


async def my_poll(message: types.Message):
    # await send_poll(message, test_group)
    await ask_session_id(message)


async def send_poll(call: types.CallbackQuery, callback_data: dict, test_group):

    quiz = callback_data["quiz"]

    QUESTION = quiz['QUESTION']
    ANSWER1 = quiz['ANSWER1']
    ANSWER2 = quiz['ANSWER2']
    ANSWER3 = quiz['ANSWER3']
    ANSWER4 = quiz['ANSWER4']

    await bot.send_message(test_group, "here 111")
    await call.bot.send_poll(test_group, question=QUESTION, options=[ANSWER1, ANSWER2, ANSWER3, ANSWER4],
                                allows_multiple_answers=False)



# async def send_poll(message: types.Message, test_group):
#     await bot.send_message(test_group, "here 111")
#     await message.bot.send_poll(test_group, question='my question', options=['qqq', 'www'],
#                                 allows_multiple_answers=False)
