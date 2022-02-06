from aiogram import types

from newapp.loader import cb, cb_number_answer


async def main_menu_inline_keyboard(text):
    buttons = [
        types.InlineKeyboardButton(text=text['main_menu'][0],
                                   callback_data="start_session"),
        types.InlineKeyboardButton(text=text['main_menu'][1],
                                   callback_data="switcher_get_data_for_user"),
        types.InlineKeyboardButton(text=text['main_menu'][2],
                                   callback_data="description"),
        types.InlineKeyboardButton(text=text['main_menu'][3],
                                   callback_data="settings")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    return keyboard


async def main_menu_usual_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["\U00002618 Main Menu", "\U00002618 Cancel"]
    keyboard.add(*buttons)

    return keyboard


async def description_menu(text):
    # await call.answer(text="\U0001F603 Buy!", show_alert=True)
    # или просто await call.answer()
    buttons = [
        types.InlineKeyboardButton(text=text['description_menu'][0],
                                   callback_data="switcher_to_main_menu") ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    return keyboard


async def send_poll_menu(session_id):
    buttons = [
        types.InlineKeyboardButton(text="Edit", callback_data=cb.new(session_id=session_id)),
        types.InlineKeyboardButton(text="Send poll", callback_data="send_poll"),
        types.InlineKeyboardButton(text="Cancel", callback_data="close_session"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    return keyboard


async def ask_for_answer_menu(text, number_answer):
    buttons = [
        types.InlineKeyboardButton(text=text['various'][0], callback_data=cb_number_answer.new(number_answer=number_answer)),
        types.InlineKeyboardButton(text=text['various'][1],
                                   callback_data="notice_to_admin")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)

    return keyboard


async def settings_menu(text):
    buttons = [
        types.InlineKeyboardButton(text=text['settings_menu'][1],
                                   callback_data="set_rus_language"),
        types.InlineKeyboardButton(text="🇬🇧 English", callback_data="set_eng_language")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)

    return keyboard




