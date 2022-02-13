

async def selected_text(lang):

    if lang == 'ru':
        return await russian_text()
    else:
        return await english_text()


async def russian_text():
    text = {'first': ['Эй', "Спроси меня и я смогу спросить весь Мир!"],
            'main_menu': ["\U00002618  Спросить Мир", "\U0001F3F5  Мой "
                                                       "последний вопрос",
                          "\U0001F4D5  Описание",
                          "\U00002699 Настройки"],
            'settings_menu': ["\U0001F4E2 Выбирите язык", "🇷🇺 Русский"],
            'description_menu': ["\U00002B05  Назад", "\U0001F4E2 Это "
                                                      "описание"],
            'last_quize': ["\U0001F49C Последний КВИЗ:", "🔸 Дата и время:",
                                              "🔸 вопрос:", "🔸 ответ 1:",
                           "🔸 ответ 2:", "🔸 ответ 3:", "🔸 ответ 4:",
                           "\U0001F916 Спроси меня еще разок \U00002B07"],
            'ask_world': ["\U0001F7E2 Отправь мне свой вопрос здесь:",
                          "Вы написали слишком короткий вопрос. Пожалуйста, "
                          "повторите попытку",
                           "Вы написали слишком большой вопрос. Пожалуйста, "
                          "повторите попытку",
                          "Вы написали слишком короткий вариант ответа. "
                          "Пожалуйста, повторите попытку",
                          "Вы написали слишком большой вариант ответа. Пожалуйста, "
                          "повторите попытку",
                          # 5:
                          "\U0001F7E1 Теперь Вам нужно написать от 2 до 4 "
                                               "вариантов ответов."
                                               "\n",
                          "Сейчас отправьте свой Первый вариант Ответа:",
                          "\U0001F7E1 Сейчас отправьте свой Второй вариант "
                          "Ответа:",
                          "Третий вариант Ответа",
                          "Четвертый вариант Ответа",
                          # 10:
                          "\U0001F7E1 Вы хотите записать свой",
                          "вариант Ответа?",
                          "Третий",
                          "Четвертый",
                          "Отправьте свой",
                          # 15:
                          "вариант Ответа:",
                          "Спасибо! Ваш КВИЗ записан и отправлен на "
                          "рассмотрение.\n"
                          "После прохождения модерации мы опубликуем его"],
            'various': ["Да", "Нет"]}
    return text


async def english_text():
    text = {'first': ['Hey', "Ask me and I can ask the whole World!"],
            'main_menu': ["\U00002618  Ask the World", "\U0001F3F5  My last "
                                                        "quiz",
                          "\U0001F4D5  Description",
                          "\U00002699 Settings"],
            'settings_menu': ["\U0001F4E2 Choose language", "🇷🇺 Russian"],
            'description_menu': ["\U00002B05  Back", "\U0001F4E2 It`s the "
                                                     "description"],
            'last_quize': ["\U0001F49C LAST QUIZ:", "🔸 Date & time:",
                                              "🔸 question:", "🔸 answer 1:",
                           "🔸 answer 2:", "🔸 answer 3:", "🔸 answer 4:",
                           "\U0001F916 Ask me one more time \U00002B07"],
            'ask_world': ["\U0001F7E2 Send me your question here:",
                          "You wrote a very short question. Please try again",
                          "You wrote a very big question. Please try again",
                          "You wrote a very short possible answer. Please try "
                          "again",
                          "You wrote a very big possible answer. Please try "
                          "again",
                          #5:
                          "\U0001F7E1 Now you need to write from 2 to 4 "
                          "possible answers.\n",
                          "Now send your First possible Answer:",
                          "\U0001F7E1 Now send your Second possible Answer:",
                          "Third possible Answer",
                          "Fourth possible Answer",
                          #10:
                          "\U0001F7E1 Do you want to write down your",
                          "possible Answer?",
                          "Third",
                          "Fourth",
                          "Send your",
                          #15:
                          "possible Answer:",
                          "Thanks! Your QUIZ has been recorded and submitted "
                          "for review\n"
                          "After passing the moderation procedure, we will "
                          "publish it"],
            'various': ["Yes", "No"]}
    return text

    # buttons = [
    #     types.InlineKeyboardButton(text="\U00002618  Ask a question", callback_data="start_session"),
    #     types.InlineKeyboardButton(text="\U0001F3F5  See my last quiz", callback_data="switcher_get_data_for_user"),
    #     types.InlineKeyboardButton(text="\U0001F4D5  Description",
    #                                callback_data="description"),
    #     types.InlineKeyboardButton(text="\U00002699 Settings", callback_data="settings")
    # ]