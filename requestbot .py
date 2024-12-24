import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from pgadminn import create_table, save_user

Token = "6894783078:AAH_pcHLYY_Byah_gjqRPhSAq6qAQfq5kWg"
channel_username = "@zzayabka"

bot = Bot(token=Token)
dp = Dispatcher()

user_data = {}

@dp.message()
async def proccess_input(message:types.Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        await start(message)
    elif 'name' not in user_data[user_id]:
        await name(message)
    elif 'phone' not in user_data[user_id]:
        await phone(message)
    elif 'age' not in user_data[user_id]:
        await age(message)
    elif message.text == 'Leave a request':
        await start(message)

@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {}
    await message.answer("Hi!\nPlease enter your name:)")

async def name(message:types.Message):
    user_id = message.from_user.id
    user_data[user_id]['name'] = message.text
    button = [
        [types.KeyboardButton(text="Send my phone number", request_contact=True)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, one_time_keyboard=True)
    await message.answer("Enter your phone number\nOr click the button:", reply_markup=keyboard)

async def phone(message:types.Message):
    user_id = message.from_user.id
    if message.contact:
        user_data[user_id]['phone'] = message.contact.phone_number
    else:
        user_data[user_id]['phone'] = message.text
    await message.answer("Please enter your age:")

async def age(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id]['age'] = message.text
    message_text = (f"Your name: {user_data[user_id]['name']}\n"
                    f"Your phone: +{user_data[user_id]['phone']}\n"
                    f"Your age: {user_data[user_id]['age']}\n")
    button = [
        [types.KeyboardButton(text='Save my info')]
    ]
    create_table()
    save_user(user_data[user_id]['name'],
              user_data[user_id]['phone'],
              user_data[user_id]['age'])
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, one_time_keyboard=True)
    await message.answer(f"Application received! We’ll review it shortly.\n"
                         f"{message_text}", reply_markup=keyboard)
    await bot.send_message(channel_username, message_text)
    del user_data[user_id]

async def main():
    print('The bot is running!')
    await dp.start_polling(bot)
asyncio.run(main())
