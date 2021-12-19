from aiogram import types


async def main_menu_inline_keyboard():
    buttons = [
        types.InlineKeyboardButton(text="\U00002618  Ask a question", callback_data="start_session"),
        types.InlineKeyboardButton(text="\U0001F3F5  See my last quiz", callback_data="switcher_get_data_for_user"),
        types.InlineKeyboardButton(text="\U0001F4D5  Description", callback_data="description"),
        types.InlineKeyboardButton(text="\U00002699 Settings", callback_data="close_session")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    return keyboard