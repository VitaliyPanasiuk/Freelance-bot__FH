from aiogram import Router, Bot, types
from aiogram.types import Message,FSInputFile
from tgbot.config import load_config
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State, StatesGroup
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
from tgbot.config import  DB_URI
from random import randint
import datetime
from tgbot.filters.authors import AuthorFilter

from tgbot.misc.states import mailing, reg_author,getOrder, private_get
from tgbot.misc.function import check_id,auf_author

from tgbot.keyboards.textBtn import typeBtn,answer_speciality
from tgbot.keyboards.inline import confirm_buttons

from tgbot.db import orders_update

import asyncio


author_router = Router()
author_router.message.filter(AuthorFilter())
config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
bot2 = Bot(token=config.tg_bot.token2, parse_mode='HTML')


@author_router.message(commands=["start"])
async def test_start(message: Message, state: FSMContext):
    print('handle in start')
    print(message.text)
    # if message.text == '/start':
    auf_status = await auf_author(str(message.from_user.id))
    btn = confirm_buttons()
    if auf_status:
        await message.reply("Вітання!", reply_markup=btn.as_markup())
    else:
        await message.reply("Привіт! 👋\nНадішли мені номер своєї карти, бажано приват універсальну (тільки не для виплат)💳")
        await state.set_state(reg_author.get_card) 
    # elif message.text.isdigit() and auf_status == False:
    #     text = message.text
    #     await state.update_data(get_card=text) 
    #     btn = answer_speciality()
    #     await bot2.send_message(message.from_user.id,'Чудово! 👍 Вкажи перелік спеціальностей, які тебе цікавлять та натисни кнопку "✅Готово"',reply_markup=btn.as_markup(resize_keyboard=True))
    #     await state.update_data(get_speciality = None) 
    #     await state.set_state(reg_author.get_speciality)  
        

@author_router.message_handler(content_types=types.ContentType.TEXT, state=private_get.money)
async def test_start(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(get_card=text) 
    btn = answer_speciality()
    await bot2.send_message(message.from_user.id,'Чудово! 👍 Вкажи перелік спеціальностей, які тебе цікавлять та натисни кнопку "✅Готово"',reply_markup=btn.as_markup(resize_keyboard=True))
    await state.update_data(get_speciality = None) 
    await state.set_state(reg_author.get_speciality)
    # await orders_update.update_answer(message.text,str(message.from_user.id))
    # await state.clear()
# @author_router.message(commands=["start"])
# async def admin_start(message: Message, state: FSMContext):

    
@author_router.message(content_types=types.ContentType.TEXT, state=reg_author.get_card)
async def admin_start(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(get_card=text) 
    btn = answer_speciality()
    await bot2.send_message(message.from_user.id,'Чудово! 👍 Вкажи перелік спеціальностей, які тебе цікавлять та натисни кнопку "✅Готово"',reply_markup=btn.as_markup(resize_keyboard=True))
    await state.update_data(get_speciality = None) 
    await state.set_state(reg_author.get_speciality)
    
@author_router.message(content_types=types.ContentType.TEXT, state=reg_author.get_speciality)
async def admin_start(message: Message, state: FSMContext):
    text = message.text
    btn = confirm_buttons()
    if text != 'Готово✅':
        answ = ''
        data = await state.get_data()
        answ = data['get_speciality']
        if answ:
            answ += '/' + text
            await state.update_data(get_speciality = answ) 
        else:
            await state.update_data(get_speciality = text) 

            
        await state.set_state(reg_author.get_speciality)
    else:
        data = await state.get_data()
        print(data['get_speciality'])
        spec = data['get_speciality'].split('/')
        await bot2.send_message(message.from_user.id,'Вітаю! 🥳',reply_markup=types.ReplyKeyboardRemove())
        await bot2.send_message(message.from_user.id,"Реєстрація пройдена. Будь на готові, скоро будуть нові замовлення.🤩",reply_markup=btn.as_markup())
        await orders_update.reg_author(str(message.from_user.id),message.from_user.first_name,data['get_card'],spec)
        await state.clear()


# @author_router.message(commands=["show"])
@author_router.callback_query(lambda c: c.data == 'show')
async def admin_start(callback_query: types.CallbackQuery, state: FSMContext):
    userid = callback_query.from_user.id
    base = psycopg2.connect(
        dbname=config.db.database,
        user=config.db.user,
        password=config.db.password,
        host=config.db.host,)
    cur = base.cursor()
    data = (str(userid),)
    cur.execute('''SELECT * FROM orders WHERE author_id = %s and status IN ('План','План готовий','План відправлено','
План затверджено','В роботі','Правки в роботі') ORDER BY priority DESC''',data)
    orders = cur.fetchall()
    for order in orders:
        money = 0
        costs = order[17].split(',')
        money += float(costs[0])
        money += float(costs[1])
        await bot2.send_message(userid,f'''                        
🆔: {order[1]}
📌**Статус**: {order[11]}
◽️ **Пріоритет**:{order[28]}
◾️ Спеціальність: {order[4]}
◽️ Вид роботи: {order[5]}
◾️ Тема: {order[7]}
◽️ Обсяг: {order[6]} ст.
◾️ Унікальність: {order[8]}
◽️ Дедлайн: {order[26]}
◾️ Коментар: {order[18]}
💸 Ціна: {money}
                                ''')
    cur.close()
    base.close()   
        

# @author_router.message(commands=["earn"])
@author_router.callback_query(lambda c: c.data == 'earn')
async def admin_start(callback_query: types.CallbackQuery, state: FSMContext):
    userid = callback_query.from_user.id
    base = psycopg2.connect(
        dbname=config.db.database,
        user=config.db.user,
        password=config.db.password,
        host=config.db.host,)
    cur = base.cursor()
    data = (str(userid),)
    cur.execute('''SELECT * FROM orders WHERE author_id = %s and status IN ('Готово/правки','Правки','Правки в роботі','Правки відправлені','Готово') ORDER BY priority DESC''',data)
    orders = cur.fetchall()
    mess = ''
    for order in orders:
        costs = order[17].split(',')
        cost_status = order[18].split(',')
        if cost_status[0] == 'false' and cost_status[1] == 'false':
            mess += f'{order[1]},{order[7]},{costs[21]},{costs[0]}\n'
        elif cost_status[0] == 'true' and cost_status[1] == 'false':
            mess += f'{order[1]},{order[7]},{costs[21]},{costs[1]}\n'
    await bot2.send_message(userid,mess)
    cur.execute('''SELECT * FROM orders WHERE author_id = %s and status IN ('Готово/правки','Правки','Правки в роботі','Правки відправлені','Готово')''',data)
    orders = cur.fetchall()
    money = 0
    for order in orders:
        costs = order[17].split(',')
        cost_status = order[18].split(',')
        if cost_status[0] == 'false' and cost_status[1] == 'false':
            money += float(costs[0])
        elif cost_status[0] == 'true' and cost_status[1] == 'false':
            money += float(costs[1]) 
    await bot2.send_message(userid,"💵Сума за тиждень: " + str(money))
    cur.close()
    base.close() 


