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

from tgbot.misc.states import mailing, reg_author
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
async def admin_start(message: Message, state: FSMContext):
    auf_status = await auf_author(str(message.from_user.id))
    btn = confirm_buttons()
    if auf_status:
        await message.reply("Вітання!", reply_markup=btn)
    else:
        await message.reply("Вітання!\nНадішліть мені номер своєї карти")
        await state.set_state(reg_author.get_card)
    
@author_router.message(content_types=types.ContentType.TEXT, state=reg_author.get_card)
async def admin_start(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(get_card=text) 
    btn = answer_speciality()
    await bot2.send_message(message.from_user.id,"Відмінно, тепер надішліть мені свою спеціальність",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.update_data(get_speciality = None) 
    await state.set_state(reg_author.get_speciality)
    
@author_router.message(content_types=types.ContentType.TEXT, state=reg_author.get_speciality)
async def admin_start(message: Message, state: FSMContext):
    text = message.text
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
        await bot2.send_message(message.from_user.id,"Відмінно, тепер ти зареєстрований ")
        await orders_update.reg_author(str(message.from_user.id),data['get_card'],spec)
        await state.clear()


@author_router.message(commands=["show"])
async def admin_start(message: Message, state: FSMContext):
    userid = message.from_user.id
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    data = (str(userid),)
    cur.execute('''SELECT * FROM orders WHERE author_id = %s ORDER BY priority DESC''',data)
    orders = cur.fetchall()
    for order in orders:
        await bot2.send_message(userid,f'''id: {order[0]}
Вид роботи: {order[5]}
Тема роботи: {order[7]}
Обсяг роботи: {order[6]} ст.
Унікальність роботи: {order[8]}
Спеціальність: {order[4]}
Коментарий: {order[18]}
Ціна: {order[16]}
                                ''')
        
        

@author_router.message(commands=["earn"])
async def admin_start(message: Message, state: FSMContext):
    userid = message.from_user.id
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    data = (str(userid),)
    cur.execute('''SELECT * FROM orders WHERE author_id = %s and status IN ('Готово/правки','Правки','Правки в роботі','Правки відправлені','Готово') and costs_status = false ORDER BY priority DESC''',data)
    orders = cur.fetchall()
    for order in orders:
        await bot2.send_message(userid,f'''id: {order[0]}
Вид роботи: {order[5]}
Тема роботи: {order[7]}
Обсяг роботи: {order[6]} ст.
Унікальність роботи: {order[8]}
Спеціальність: {order[4]}
Коментарий: {order[18]}
Ціна: {order[16]}
                                ''')
    cur.execute('''SELECT * FROM orders WHERE author_id = %s and status IN ('Готово/правки','Правки','Правки в роботі','Правки відправлені','Готово') and costs_status = false''',data)
    orders = cur.fetchall()
    money = 0
    for order in orders:
        if order[16]:
            money += order[16]
    await bot2.send_message(userid,"Ваш заробіток становитиме: " + money)

