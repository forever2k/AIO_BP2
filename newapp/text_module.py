import random

def define_word(list):
    num = random.randint(0, len(list)-1)
    return list[num]


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
            'description_menu': ["\U00002B05  Назад",
                                 "\U0001F4E2  Хотите узнать мнение других людей в отношении своего личного вопроса, но при этом остаться анонимным\U00002753 \U0001F440 \n\n"
                                 "\U0001F4A0  Тогда оставьте боту-помощнику свой вопрос и от 2 до 4 возможных вариантов ответов - КВИЗ.\n"
                                 "\U0001F4A0  После того как вопрос и ответы "
                                 "будут проверены модератором, они будут "
                                 "опубликованы в общем чате, где все желающие участники смогут выбрать (проголосовать за) один понравившийся вариант ответа.\n"
                                 "\U0001F4A0  Вам останется лишь наблюдать со стороны за результатами КВИЗа.\n"
                                 "\U0001F4A0  Дополнительно все желающие, "
                                 "в том числе и Вы, можете оставлять "
                                 "комментарии для любого КВИЗа и/или дополнять "
                                 "информацию \U0001F525 \n"
                                 "\U0001F4A0  Время для голосавания ограничено 24 часами \U000023F3 \n\n"
                                 "\U0000203C  ЗАПРЕЩЕНО: спам, флуд, "
                                 "любого рода оскорбления, расизм и реклама. \U0000203C \n\n"
                                 "\U0001F4A0  Попробуй прямо сейчас! /start \U0001F929 \U0001F929 \U0001F929"],
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
                          "Вы хотите записать свой",
                          "вариант Ответа?",
                          "Третий",
                          "Четвертый",
                          "\U0001F7E1 Сейчас отправьте свой",
                          # 15:
                          "вариант Ответа:",
                          f"Спасибо! Ваш {define_word(['чудесный', 'классный', 'очаровательный', 'восхитительный'])} КВИЗ отправлен на рассмотрение.\n"
                          "После прохождения модерации мы опубликуем его"],
            'various': ["Да", "Нет"],
            'close_session': ["Сессия завершена", "\U0001F603 Пока!"]}
    return text


async def english_text():
    text = {'first': ['Hey', "Ask me and I can ask the whole World!"],
            'main_menu': ["\U00002618  Ask the World", "\U0001F3F5  My last "
                                                        "quiz",
                          "\U0001F4D5  Description",
                          "\U00002699 Settings"],
            'settings_menu': ["\U0001F4E2 Choose the language", "🇷🇺 Russian"],
            'description_menu': ["\U00002B05  Back",
                                 "\U0001F4E2  Do you want to know the opinion of other people regarding your personal question, but at the same time remain anonymous\U00002753 \U0001F440 \n\n"
                                 "\U0001F4A0  Then leave your question to the assistant bot and from 2 to 4 possible answers - a QUIZ.\n"
                                 "\U0001F4A0  After the question and answers "
                                 "are checked by the moderator, they will be "
                                 "published in the general chat, where all "
                                 "interested participants will be able to "
                                 "choose (vote for) one answer option they like.\n"
                                 "\U0001F4A0  You will only have to observe the results of the QUIZ from the side.\n"
                                 "\U0001F4A0  Additionally, everyone, "
                                 "including you, can leave comments for any "
                                 "quiz and/or supplement the information \U0001F525 \n"
                                 "\U0001F4A0  Voting time is limited to 24 hours \U000023F3 \n\n"
                                 "\U0000203C  PROHIBITED: spam, flood, "
                                 "any kind of insults, racism and advertising. "
                                 "\U0000203C \n\n"
                                 "\U0001F4A0  Try it right now! /start \U0001F929 \U0001F929 \U0001F929"],
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
                          "Do you want to write down your",
                          "possible Answer?",
                          "Third",
                          "Fourth",
                          "\U0001F7E1 Now send your",
                          #15:
                          "possible Answer:",
                          f"Thanks! Your {define_word(['wonderful', 'cool', 'charming', 'delightful'])} QUIZ has been submitted for review.\n"
                          "After passing the moderation procedure, we will "
                          "publish it"],
            'various': ["Yes", "No"],
            'close_session': ["Session is finished", "\U0001F603 Buy!"]}
    return text

    # buttons = [
    #     types.InlineKeyboardButton(text="\U00002618  Ask a question", callback_data="start_session"),
    #     types.InlineKeyboardButton(text="\U0001F3F5  See my last quiz", callback_data="switcher_get_data_for_user"),
    #     types.InlineKeyboardButton(text="\U0001F4D5  Description",
    #                                callback_data="description"),
    #     types.InlineKeyboardButton(text="\U00002699 Settings", callback_data="settings")
    # ]