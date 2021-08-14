import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import exceptions
from newapp.bt import bot
from newapp.config import dbase, test_group, me
from newapp.todo import generate_number


# available_questions = ["вопрос1", "вопрос3", "вопрос3"]
# available_answers = ["ответ1", "ответ2", "ответ3"]


cursor = dbase.cursor()

class GetData(StatesGroup):
    waiting_for_question = State()
    waiting_for_answer = State()


async def start_session(call: types.CallbackQuery):
    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # for name in available_questions:
    #     keyboard.add(name)
    # await call.message.answer("Send me your question:", reply_markup=keyboard)
    await call.message.answer("Send me your question:")
    await GetData.waiting_for_question.set()
    # await call.answer(text="Thanks!", show_alert=True)
    # или просто await call.answer()


async def get_question(message: types.Message, state: FSMContext):
    if len(message.text) < 5:
        await message.answer("Пожалуйста, напишите корректный вопрос, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_question=message.text.lower())

    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # for size in available_answers:
    #     keyboard.add(size)
    await GetData.waiting_for_answer.set()
    # await message.answer("Now write your ANSWER", reply_markup=keyboard)
    await message.answer("Now write your ANSWER")



async def get_answer(message: types.Message, state: FSMContext):
    if len(message.text) < 5:
        await message.answer("Пожалуйста, напишите вопрос, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_answer=message.text.lower())
    user_data = await state.get_data()
    await message.answer(f"Вы написали вопрос: {user_data['chosen_question']}.\n"
                         f"Вы написали ответ: {user_data['chosen_answer']}.\n"
                         f"Попробуйте теперь задать еще вопрос: /start", reply_markup=types.ReplyKeyboardRemove())

    user_id = message.from_user.id
    # bd_id = generate_number(user_id)
    bd_id = "343464574564"

    try:

        sql = "INSERT INTO users (bd_id, user_id, QUESTION, ANSWER) \
                                                          VALUES (%s, %s, %s, %s)"
        val = (bd_id, user_id, user_data['chosen_question'], user_data['chosen_answer'])
        cursor.execute(sql, val)
        dbase.commit()

    except Exception as e:
        await message.reply(message, 'Something went wrong.. Please contact the admin')

    try:
        await message.answer("it`s the last part")
        await bot.send_message(test_group, "A new message has been received", disable_notification=False)
        # await bot.send_message(test_group, 'New question was recevied')
        # await bot.send_message(me, 'New question was recevied')

    except exceptions.BotBlocked:
        logging.error(f"Target [ID:{test_group}]: blocked by user")

    await state.finish()
