from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup



class GetData(StatesGroup):
    waiting_for_question = State()
    waiting_for_answer1 = State()


async def get_question(message: types.Message, state: FSMContext):
    await state.update_data(chosen_question=message.text.lower())
    await GetData.next()
    await message.answer("Now write your ANSWER 1")


async def get_answers1(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(f"Вы написали вопрос: {user_data['chosen_question']}.\n"
                         f"Попробуйте теперь задать еще вопрос: /start", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
