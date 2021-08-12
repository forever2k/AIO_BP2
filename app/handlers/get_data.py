from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


# available_questions = ["вопрос1", "вопрос3", "вопрос3"]
# available_answers = ["ответ1", "ответ2", "ответ3"]

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
    # await GetData.waiting_for_answer.set()
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
    await state.finish()
