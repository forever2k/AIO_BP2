import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import BotCommand
from aiogram.utils.executor import start_webhook
import mysql.connector
from random import randint
from aiogram.utils.exceptions import BotBlocked

from app.handlers.common import register_handlers_common


test_group = -1001153348142
test = -1001364950026

me = os.getenv('me')

TOKEN = os.getenv('TOKEN')
PROJECT_NAME = os.getenv('PROJECT_NAME')

WEBHOOK_HOST = f'https://{PROJECT_NAME}.herokuapp.com'
WEBHOOK_PATH = '/' + TOKEN
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.environ.get('PORT')


dbase = mysql.connector.connect(
        host=os.getenv('myhost'),
        user=os.getenv('myuser'),
        passwd=os.getenv('mypass'),
        port="3306",
        database="bqcbwpmrbqj7ghxx")

