from create_bot import bot, dp
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

urlkb = InlineKeyboardMarkup(row_width=2)
urlButton1 = InlineKeyboardButton(text='Link1', url='youtube.com')
urlButton2 = InlineKeyboardButton(text='Link2', url='google.com')
urlkb.add(urlButton1, urlButton2)


# @dp.message_handler(commands=['Links'])
async def send_links(message: types.Message):
    await message.answer('Links', reply_markup=urlkb)


callinkb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Press me', callback_data='www'),
                                                 InlineKeyboardButton(text='Press me 2', callback_data='ttt'))


# @dp.message_handler(commands=['test'])
async def test_command(message: types.Message):
    await message.answer('Test', reply_markup=callinkb)


# @dp.callback_query_handler(text='www')
async def call_www(callback: types.CallbackQuery):
    await callback.answer('Button pressed')


# @dp.callback_query_handler(text='ttt')
async def call_ttt(callback: types.CallbackQuery):
    await callback.answer('Button pressed', show_alert=True)


def register_handlers_inline_kb(dp: Dispatcher):
    dp.register_message_handler(send_links, commands=['Links'])
    dp.register_message_handler(test_command, commands=['test'])
    dp.register_callback_query_handler(call_www, text='www')
    dp.register_callback_query_handler(call_ttt, text='ttt')
