from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext

from newapp.config import TOKEN



bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


