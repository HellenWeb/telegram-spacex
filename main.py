
# Modules
import requests
from aiogram import types, executor
from dispacher import dp, bot

# Logic

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    mark = types.InlineKeyboardMarkup(row_width=1)
    mark.add(types.InlineKeyboardButton(text="Help", callback_data='help'))
    await message.answer(f"Hello <strong>{message.from_user.first_name}</strong>\n\n<strong>This Bot is linked to the SpaceX API and has posted information directly with it</strong>\n\nCreator: @YungHellen", reply_markup=mark, parse_mode='html')

@dp.message_handler(commands=['about_company'])
async def about_company(message: types.Message):
    res = requests.get("https://api.spacexdata.com/v4/company")
    await message.answer(f'Name = <strong>{res.json()["name"]}</strong>\nFouder = <strong>{res.json()["founder"]}</strong>\nDescription = <strong>{res.json()["summary"]}</strong>', parse_mode='html')

# Callbacks

@dp.callback_query_handler(lambda r: r.data == "help")
async def call_help(callback: types.CallbackQuery):
    mark = types.InlineKeyboardMarkup(row_width=1)
    mark.add(types.InlineKeyboardButton(text="Back", callback_data='back'))
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text="<strong>/start</strong> = Welcome Message\n<strong>/help</strong> = All Commands", reply_markup=mark, parse_mode='html')

@dp.callback_query_handler(lambda m: m.data == "back")
async def call_back(callback: types.CallbackQuery):
    mark = types.InlineKeyboardMarkup(row_width=1)
    mark.add(types.InlineKeyboardButton(text="Help", callback_data='help'))
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=f"Hello <strong>{callback.message.from_user.first_name}</strong>\n\n<strong>This Bot is linked to the SpaceX API and has posted information directly with it</strong>\n\nCreator: @YungHellen", reply_markup=mark, parse_mode='html')

# Polling

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)