import datetime
import logging
from aiogram import types
from newapp.bt import bot
from config import test_group, test_channel
from newapp.handlers.get_data_from_database import ask_session_id
from newapp.loader import admin_data

async def my_poll(message: types.Message):
    # await send_poll(message, test_group)
    await ask_session_id(message)


async def send_poll(call: types.CallbackQuery, test_channel=test_channel, admin_data=admin_data):

    session_id = admin_data['session_id']
    QUESTION = admin_data['question']
    ANSWER1 = admin_data["answer1"]
    ANSWER2 = admin_data["answer2"]
    ANSWER3 = admin_data["answer3"]
    ANSWER4 = admin_data["answer4"]

    close_date = datetime.datetime.now() + datetime.timedelta(minutes=11)

    options = []

    if admin_data["answer1"]:
        options.append(admin_data["answer1"])
    if admin_data["answer2"]:
        options.append(admin_data["answer2"])
    if admin_data["answer3"]:
        options.append(admin_data["answer3"])
    if admin_data["answer4"]:
        options.append(admin_data["answer4"])

    try:
        text = "►►► SEND YOUR OWN POLL HERE ◄◄◄"

        markup = types.InlineKeyboardMarkup()
        switch_button = types.InlineKeyboardButton(text=text, url='https://t.me/Btf2NeDetBot?start')
        markup.add(switch_button)

        await call.bot.send_poll(test_channel, question=QUESTION, options=options,
                                 allows_multiple_answers=False, close_date=close_date,
                                 reply_markup=markup)

        # await bot.send_message(test_channel, '<i>*** Do you want to see your own poll here? ***</i>', reply_markup=markup, parse_mode=types.ParseMode.HTML)

    except Exception as e:
        await call.message.answer("We could not send the Poll :(  Maybe don`t enough answers")



# async def send_poll(message: types.Message, test_group):
#     await bot.send_message(test_group, "here 111")
#     await message.bot.send_poll(test_group, question='my question', options=['qqq', 'www'],
#                                 allows_multiple_answers=False)
