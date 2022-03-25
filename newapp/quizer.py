import datetime
import logging
from aiogram import types
from newapp.bt import bot
from config import test_group, test_channel
from newapp.handlers.get_data_from_database import ask_session_id
from newapp.loader import admin_data

async def my_poll(message: types.Message):
    await ask_session_id(message)


async def send_poll(call: types.CallbackQuery, test_channel=test_channel, admin_data=admin_data):

    # session_id = admin_data['session_id']
    QUESTION = admin_data['question']
    ANSWER1 = admin_data["answer1"]
    ANSWER2 = admin_data["answer2"]
    ANSWER3 = admin_data["answer3"]
    ANSWER4 = admin_data["answer4"]

    close_date = datetime.datetime.now() + datetime.timedelta(minutes=1)

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
        text = "►►► ОТПРАВИТЬ МОЙ КВИЗ ◄◄◄"

        markup = types.InlineKeyboardMarkup()
        switch_button = types.InlineKeyboardButton(text=text, url='https://t.me/Btf2NeDetBot?start')
        markup.add(switch_button)

        await bot.send_poll(test_channel, question=QUESTION, options=options,
                                 allows_multiple_answers=False, close_date=close_date,
                                 reply_markup=markup)

    except Exception as e:
        await bot.send_message(test_group,
                               f"There is a mistake in modul - 'send_poll':"
                               f" {e}")
        await call.message.answer("We could not send the QUIZ :(  Maybe don`t "
                                  "enough answers")
