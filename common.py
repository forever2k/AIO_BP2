from random import randint
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.utils.exceptions import BotBlocked


# @dp.message_handler(commands=['start'], state="*")




# @dp.message_handler(commands=['start'], state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Hi my friend! \n"
                         "Ask me and I can ask the whole World!",
                         reply_markup=types.ReplyKeyboardRemove()
    )
    await ask_start(message)



async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Action canceled", reply_markup=types.ReplyKeyboardRemove())



async def ask_start(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="YES!", callback_data="start_session"),
        types.InlineKeyboardButton(text="NO :(", callback_data="close_session")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Are you ready?", reply_markup=keyboard)







async def close_session(call: types.CallbackQuery):
    await call.message.answer("It`s the close_session")
    await call.answer(text="Buy!", show_alert=True)
    # или просто await call.answer()



async def cmd_random(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Press me", callback_data="random_value"))
    await message.answer("Number from 1 to 10", reply_markup=keyboard)


async def send_random_value(call: types.CallbackQuery):
    await call.message.answer(str(randint(1, 10)))
    await call.answer(text="Thanks!", show_alert=True)
    # или просто await call.answer()



# обработчик исключения BotBlocked
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    # Update: объект события от Telegram. Exception: объект исключения
    # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")

    # Такой хэндлер должен всегда возвращать True,
    # если дальнейшая обработка не требуется.
    return True


# Просто функция, которая доступна только администратору,
# чей ID указан в файле конфигурации.
async def secret_command(message: types.Message):
    await message.answer("Поздравляю! Эта команда доступна только администратору бота.")


