import logging
from aiogram import types
from newapp.bt import bot
from config import test_group

async def my_poll(message: types.Message):
    await send_poll(message, test_group)

async def send_poll(message: types.Message, test_group):
    await bot.send_message(test_group, "here 111")
    await message.bot.send_poll(test_group, question='my question', options=['qqq', 'www'],
                                allows_multiple_answers=False)
