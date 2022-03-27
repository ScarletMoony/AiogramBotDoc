from aiogram import executor
from create_bot import dp
from inlinekb import inline_kb

from handlers import client, admin, other

from DB import bot_db

import json, string

def on_bot_start():
    print('Bot is up')

# bot_db.create_db()


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)
inline_kb.register_handlers_inline_kb(dp)


# @dp.message_handler(commands=['start', 'help'])
# async def start_commands(message: types.Message):
#     try:
#         await bot.send_message(message.from_user.id, 'Welcome to my chat')
#         await message.delete()
#     except:
#         await message.reply('Please PM me for info\nt.me/MyBotDocbot')
#         await message.delete()

# @dp.message_handler()
# async def echo_reply(message: types.Message):
#     await message.answer(message.text)

# @dp.message_handler()
# async def echo_reply(message: types.Message):
#     if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
#         .intersection(set(json.load(open('ban_word_list.json')))) != set():
#         await message.reply('Language')
#         await message.delete()

if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_bot_start())