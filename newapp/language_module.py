from aiogram.dispatcher import FSMContext
from newapp.loader import *
from newapp.config import dbase
from aiogram import Dispatcher, types, md
from newapp.menu_switchers import switcher_to_main_menu

cursor = dbase.cursor()

async def check_user_settings_exists(user_id):

    user_id_exists = "SELECT COUNT(*) FROM user_settings WHERE user_id = %s"
    cursor.execute(user_id_exists, (user_id,))
    results_user_exists = cursor.fetchone()

    return results_user_exists[0]


async def set_users_dictionary(user_id, user_data_settings=user_data_settings, **kwargs):
    user_data_settings[user_id] = User_settings()
    user = user_data_settings[user_id]

    for key, val in kwargs.items():
        if key == 'lang':
            user.language = val

async def set_default_language(message: types.Message, user_data_settings=user_data_settings):
    locale = message.from_user.locale
    user_id = message.from_user.id

    results_user_exists = await check_user_settings_exists(user_id)

    if results_user_exists > 0:
        user_language = "SELECT rus_language FROM user_settings WHERE user_id = %s"
        cursor.execute(user_language, (user_id,))
        results_user_language = cursor.fetchone()

        if results_user_language[0] == 1:
            await set_users_dictionary(user_id, lang='rus')
        else:
            await set_users_dictionary(user_id, lang='eng')

    else:
        if locale.english_name == 'Russian':
            default_language = "INSERT INTO user_settings (user_id, rus_language) \
                                                                  VALUES (%s, %s)"
            val = (user_id, True)
            cursor.execute(default_language, val)
            dbase.commit()

            await set_users_dictionary(user_id, lang='rus')

        else:
            default_language = "INSERT INTO user_settings (user_id, eng_language) \
                                                                          VALUES (%s, %s)"
            val = (user_id, True)
            cursor.execute(default_language, val)
            dbase.commit()

            await set_users_dictionary(user_id, lang='eng')


async def set_rus_language(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    results_user_exists = await check_user_settings_exists(user_id)

    if results_user_exists > 0:
        update_language = "UPDATE user_settings SET rus_language = %s, eng_language = %s WHERE user_id = %s"
        val = (True, False, user_id)
        cursor.execute(update_language, val)
        dbase.commit()

    else:
        set_language = "INSERT INTO user_settings (user_id, rus_language) \
                                                                              VALUES (%s, %s)"
        val = (user_id, True)
        cursor.execute(set_language, val)
        dbase.commit()

    await set_users_dictionary(user_id, lang='rus')

    await switcher_to_main_menu(call, state)


async def set_eng_language(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    results_user_exists = await check_user_settings_exists(user_id)

    if results_user_exists > 0:
        update_language = "UPDATE user_settings SET rus_language = %s, eng_language = %s WHERE user_id = %s"
        val = (False, True, user_id)
        cursor.execute(update_language, val)
        dbase.commit()
    else:
        set_language = "INSERT INTO user_settings (user_id, eng_language) \
                                                                              VALUES (%s, %s)"
        val = (user_id, True)
        cursor.execute(set_language, val)
        dbase.commit()

    await set_users_dictionary(user_id, lang='eng')

    await switcher_to_main_menu(call, state)



async def check_language(message: types.Message):
    locale = message.from_user.locale

    await message.reply(md.text(
        md.bold('Info about your language:'),
        md.text('🔸', md.bold('Code:'), md.code(locale.language)),
        md.text('🔸', md.bold('Territory:'), md.code(locale.territory or 'Unknown')),
        md.text('🔸', md.bold('Language name:'), md.code(locale.language_name)),
        md.text('🔸', md.bold('English language name:'), md.code(locale.english_name)),
        sep='\n',
    ))