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

from tgbot.keyboards.textBtn import typeBtn

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
    if auf_status:
        await message.reply("Привет!")
    else:
        await message.reply("Привет!\nОтправь мне номер своей карты")
        await state.set_state(reg_author.get_card)
    
@author_router.message(content_types=types.ContentType.TEXT, state=reg_author.get_card)
async def admin_start(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(get_card=text) 
    
    await bot2.send_message(message.from_user.id,"Отлично, теперь отправь мне свои специальности через запятую")
    await state.set_state(reg_author.get_speciality)
    
@author_router.message(content_types=types.ContentType.TEXT, state=reg_author.get_speciality)
async def admin_start(message: Message, state: FSMContext):
    text = message.text
    texts = text.replace(' ', '')
    texts = texts.split(',')
    
    await state.update_data(get_speciality=texts) 
    data = await state.get_data()

    await bot2.send_message(message.from_user.id,"Отлично, теперь ты зарегистрирован ")
    await orders_update.reg_author(str(message.from_user.id),data['get_card'],data['get_speciality'])

    await state.clear()


@author_router.message(commands=["show"])
async def admin_start(message: Message, state: FSMContext):
    userid = message.from_user.id
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    data = (str(userid),)
    cur.execute('''SELECT * FROM orders WHERE author_id = %s ''',data)
    orders = cur.fetchall()
    for order in orders:
        await bot2.send_message(userid,f'''
id: {order[0]}
date: {order[2]}
contacts: {order[3]}
type: {order[5]}
pages: {order[6]}
topic: {order[7]}
comment: {order[18]}
                                ''')
        
        

@author_router.message(commands=["earn"])
async def admin_start(message: Message, state: FSMContext):
    userid = message.from_user.id
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    data = (str(userid),)
    cur.execute('''SELECT * FROM orders WHERE author_id = %s and status IN ('Готово/правки','Правки','Правки в роботі','Правки відправлені','Готово') and costs_status = false''',data)
    orders = cur.fetchall()
    money = 0
    for order in orders:
        if order[16]:
            money += order[16]
    await bot2.send_message(userid,money)

