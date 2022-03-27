from aiogram import types, Dispatcher
from create_bot import dp

# @dp.message_handler(commands=['other'])
async def other_command(message: types.Message):
    await message.reply('Other')

def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(other_command, commands=['other'])