
# Modules

import requests
from aiogram import Bot, Dispatcher
from config import token
import logging

# Logging

logging.basicConfig(level=logging.INFO)

# Default Variebles

bot = Bot(token)
dp = Dispatcher(bot)
