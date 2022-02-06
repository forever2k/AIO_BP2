from random import randint

from aiogram.utils.callback_data import CallbackData


def generate_number(id):
    id_generate = str(id) + "_"
    for i in range(0, 6):
        id_generate = id_generate + str(randint(1, 9))
    return id_generate


user_data = {}
user_data_settings = {}
admin_data = {}

class User:
    def __init__(self):
        self.question = ''
        self.answer1 = ''
        self.answer2 = ''
        self.answer3 = ''
        self.answer4 = ''
        self.session_id = ''

class User_settings:
    def __init__(self):
        self.language = ''

class Admin:
    def __init__(self):
        self.question = ''
        self.answer1 = ''
        self.answer2 = ''
        self.answer3 = ''
        self.answer4 = ''
        self.session_id = ''


cb = CallbackData("transfer_session_id", "session_id")
cb_number_answer = CallbackData("transfer_number_of_answer", "number_answer")