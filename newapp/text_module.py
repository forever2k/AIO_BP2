

async def selected_text(lang):

    if lang == 'ru':
        return await russian_text()
    else:
        return await english_text()


async def russian_text():
    text = {'First': ['Эй', "Спроси меня и я смогу спросить весь Мир!"]}
    return text


async def english_text():
    text = {'First': ['Hey', "Ask me and I can ask the whole World!"]}
    return text

