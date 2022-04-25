# Modules
import json

import requests
from aiogram import types, executor
from dispacher import dp, bot

# Logic


@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    mark = types.InlineKeyboardMarkup(row_width=1)
    mark.add(types.InlineKeyboardButton(text="Help", callback_data="help"))
    await message.answer(
        f"Hello <strong>{message.from_user.first_name}</strong>\n\n<strong>This Bot is linked to the SpaceX API and has posted information directly with it</strong>\n\nCreator: @YungHellen",
        reply_markup=mark,
        parse_mode="html",
    )


@dp.message_handler(commands=["about_company"])
async def about_company(message: types.Message):
    res = requests.get("https://api.spacexdata.com/v4/company")
    await message.answer(
        f'Name = <strong>{res.json()["name"]}</strong>\nFouder = <strong>{res.json()["founder"]}</strong>\nDescription = <strong>{res.json()["summary"]}</strong>',
        parse_mode="html",
    )

@dp.message_handler(commands=['crew'])
async def crew(message: types.Message):
    res = requests.get('https://api.spacexdata.com/v4/crew')
    for name in res.json():
        await message.answer(f'Name = {name["name"]}\nAgency = {name["agency"]}\nPhoto = {name["image"]}')

@dp.message_handler(commands=['rockets'])
async def rocket(message: types.Message):
    res = requests.get("https://api.spacexdata.com/v4/rockets")
    mark = types.InlineKeyboardMarkup(row_width=True)
    for i in res.json():
        mark.row(
            types.InlineKeyboardButton(text=i["name"], callback_data=i["name"])
        )
    await message.answer(f"SELECT:", reply_markup=mark)

# Callbacks

@dp.callback_query_handler(lambda c: True)
async def rocket(c: types.CallbackQuery):
    res = requests.get("https://api.spacexdata.com/v4/rockets")
    for i in res.json():
        if c.data == i["name"]:
            await bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text=f'Name = {i["name"]}\nCompany = {i["company"]}\nActive = {i["active"]}\nPhoto = {i["flickr_images"][0]}')
    if c.data == "help":
        mark = types.InlineKeyboardMarkup(row_width=1)
        mark.add(types.InlineKeyboardButton(text="Back", callback_data="back"))
        await bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text="<strong>/start</strong> = Welcome Message\n<strong>/help</strong> = All Commands\n<strong>/about_company</strong> = All about SpaceX\n<strong>/crew</strong> = Composition of the whole team\n<strong>/rockets</strong> = List of all SpaceX rockets",
            reply_markup=mark,
            parse_mode="html",
        )
    if c.data == "back":
        mark = types.InlineKeyboardMarkup(row_width=1)
        mark.add(types.InlineKeyboardButton(text="Help", callback_data="help"))
        await bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=f"Hello <strong>{c.message.from_user.first_name}</strong>\n\n<strong>This Bot is linked to the SpaceX API and has posted information directly with it</strong>\n\nCreator: @YungHellen",
            reply_markup=mark,
            parse_mode="html",
        )


# Polling

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
