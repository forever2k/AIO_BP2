

async def selected_text(lang):

    if lang == 'ru':
        return await russian_text()
    else:
        return await english_text()


async def russian_text():
    text = {'first': ['Эй', "Спроси меня и я смогу спросить весь Мир!"],
            'main_menu': ["\U00002618  Задать вопрос", "\U0001F3F5  Мой "
                                                       "последний вопрос",
                          "\U0001F4D5  Описание",
                          "\U00002699 Настройки"],
            'settings_menu': ["\U0001F4E2 Выбирите язык", "🇷🇺 Русский"],
            'description_menu': ["\U00002B05  Назад", "\U0001F4E2 Это "
                                                      "описание"],

            'last_quize': ["\U0001F929 Последний КВИЗ:", "🔸 Дата и время:",
                                              "🔸 вопрос:", "🔸 ответ 1:",
                           "🔸 ответ 2:", "🔸 ответ 3:", "🔸 ответ 4:", "🔸 Что "
                                                                        "хотите еще?"]}
    return text


async def english_text():
    text = {'first': ['Hey', "Ask me and I can ask the whole World!"],
            'main_menu': ["\U00002618  Ask a question", "\U0001F3F5  My last "
                                                        "quiz",
                          "\U0001F4D5  Description",
                          "\U00002699 Settings"],
            'settings_menu': ["\U0001F4E2 Choose language", "🇷🇺 Russian"],
            'description_menu': ["\U00002B05  Back", "\U0001F4E2 It`s the "
                                                     "description"],
            'last_quize': ["\U0001F929 LAST QUIZ:", "🔸 Date & time:",
                                              "🔸 question:", "🔸 answer 1:",
                           "🔸 answer 2:", "🔸 answer 3:", "🔸 answer 4:",
                           "🔸 What do you want else?"]}
    return text

    buttons = [
        types.InlineKeyboardButton(text="\U00002618  Ask a question", callback_data="start_session"),
        types.InlineKeyboardButton(text="\U0001F3F5  See my last quiz", callback_data="switcher_get_data_for_user"),
        types.InlineKeyboardButton(text="\U0001F4D5  Description",
                                   callback_data="description"),
        types.InlineKeyboardButton(text="\U00002699 Settings", callback_data="settings")
    ]