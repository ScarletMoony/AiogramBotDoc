from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from sqlalchemy.exc import IntegrityError
from create_bot import dp, bot
from DB import bot_db

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    power = State()
    id = State()

admin_ids = set()

# @dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_new_post(message: types.Message):
    global admin_ids

    for i in bot_db.session.query(bot_db.Admin):
        # if i.admin_id not in admin_ids:
        admin_ids.add(i.admin_id)
        # print(admin_ids)

    if str(message.from_user.id) in admin_ids:
        print(admin_ids)
        # print(message.from_user.id, admin_ids, '1')
        await bot.send_message(message.from_user.id, 'Listening')
        await message.delete()
    elif str(message.from_user.id) not in admin_ids:
        # print(message.from_user.id, admin_ids, '2')
        admin = bot_db.Admin(message.from_user.first_name, message.from_user.id)
        bot_db.session.add(admin)
        bot_db.session.commit()
        await bot.send_message(message.from_user.id, 'Listening')
        await message.delete()


# @dp.message_handler(commands=['Load'], state=None)
async def load_new_hero(message: types.Message):
    print(admin_ids)
    if str(message.from_user.id) in admin_ids:
        await FSMAdmin.photo.set()
        await bot.send_message(message.from_user.id, 'Load photo')
    else:
        await message.reply('You must be moderator to load heroes\nUse /moderator to load if you are moderator')


# @dp.message_handler(state='*', commands='stop')
# @dp.message_handler(Text(equals='stop', ignore_case=True), state='*')
async def stop_load(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')


# @dp.message_handler(content_types='photo', state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply('Now enter name')


# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply('Now enter power of hero')


# @dp.message_handler(state=FSMAdmin.power)
async def load_power(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['power'] = message.text
    await FSMAdmin.next()
    await message.reply('Now enter id')


# @dp.message_handler(state=FSMAdmin.id)
async def load_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = int(message.text)

    hero_name = set()

    async with state.proxy() as data:
        # print(str(data))
        print(data.get('name'))

        for i in bot_db.session.query(bot_db.Hero):
            # if i.admin_id not in admin_ids:
            hero_name.add(i.hero_name)
            print(hero_name, i.hero_name)
        if data.get('name') not in hero_name:
            print(data.get('name'), hero_name, '2')
            hero = bot_db.Hero(data.get('id'), data.get('name'), data.get('power'), data.get('photo'))
            bot_db.session.add(hero)
            bot_db.session.commit()
            await message.reply(f'Hero {data.get("name")} is added succesfuly')
            await state.finish()
        else:
            await message.reply('Hero already exists')
            await state.finish()

    # async with state.proxy() as data:
    #     await message.reply(str(data))
    # await state.finish()


# @dp.message_handler(state='*', commands='stop')
# @dp.message_handler(Text(equals='stop', ignore_case=True), state='*')
# async def stop_load(message: types.Message, state: FSMContext):
#     if message.from_user.id == ID:
#         current_state = await state.get_state()
#         if current_state == None:
#             return
#         await state.finish()
#         await message.reply('OK')

# @dp.message_handler(commands=['admin'])
async def admin_command(message: types.Message):
    await message.reply('Admin')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_command, commands=['admin'])
    dp.register_message_handler(make_new_post, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(load_new_hero, commands=['Load'], state=None)
    dp.register_message_handler(stop_load, state="*", commands=['stop'])
    dp.register_message_handler(stop_load, Text(equals='stop', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types='photo', state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_power, state=FSMAdmin.power)
    dp.register_message_handler(load_id, state=FSMAdmin.id)
    dp.register_message_handler(stop_load, state="*", commands=['stop'])
    dp.register_message_handler(stop_load, Text(equals='stop', ignore_case=True), state="*")
