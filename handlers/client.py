from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
from DB import bot_db
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from sqlalchemy.exc import NoResultFound

class FSMHero(StatesGroup):
    get_hero = State()
    hero_to_get = State()


# @dp.message_handler(commands=['client'])
async def client_command(message: types.Message):
    await message.reply('Client', reply_markup=kb_client)


# @dp.message_handler(commands=['newest_hero'])
async def newest_hero_command(message: types.Message):
    last_id = set()
    for i in bot_db.session.query(bot_db.Hero):
        last_id.add(i.hero_id)
    last_hero = bot_db.session.query(bot_db.Hero).filter_by(hero_id = max(last_id)).one()
    print(last_hero.hero_id)
    await bot.send_photo(message.chat.id, photo=last_hero.hero_photo_id)
    await message.reply(f'Hero name: {last_hero.hero_name}\nHero power level is {last_hero.hero_power_level}\nID: {last_hero.hero_id}')

# @dp.message_handler(commands=['hero'], state=None)
async def hero_command(message: types.Message):
    await FSMHero.get_hero.set()
    await message.reply('Enter hero name')
    await FSMHero.next()


# @dp.message_handler(state=FSMHero.hero_to_get)
async def get_hero_command(message: types.Message, state: FSMContext):
    try:
        hero = bot_db.session.query(bot_db.Hero).filter_by(hero_name=message.text).one()
        print(hero.hero_name)
        await bot.send_photo(message.chat.id, photo=hero.hero_photo_id)
        await message.reply(f'Hero name: {hero.hero_name}\nHero power level is {hero.hero_power_level}\nID: {hero.hero_id}')
        await state.finish()
    except NoResultFound:
        await message.reply(f'There is no such hero named {message.text}')



# @dp.message_handler(lambda message: 'Hoho' in message.text, ignore_case=True)
async def hoho_catcher(message: types.Message):
    await message.reply('hehe')

# @dp.message_handler(commands=['end'])
async def end_command(message: types.Message):
    await message.reply('Menu closed', reply_markup=ReplyKeyboardRemove())

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(client_command, commands=['client'])
    dp.register_message_handler(end_command, commands=['end'])
    dp.register_message_handler(newest_hero_command, commands=['newest_hero'])
    dp.register_message_handler(get_hero_command, state=FSMHero.hero_to_get)
    dp.register_message_handler(hero_command, commands=['hero'], state=None)
    dp.register_message_handler(hoho_catcher, lambda message: 'hoho' in message.text)
