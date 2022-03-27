from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('/client')
b2 = KeyboardButton('/admin')
b3 = KeyboardButton('/other')
b4 = KeyboardButton('/end')
# b5 = KeyboardButton('/mynumber', request_contact=True)
# b6 = KeyboardButton('/mylocation', request_location=True)


kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(b1).row(b2, b3).add(b4)#.add(b5).insert(b6)