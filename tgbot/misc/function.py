from asyncio.windows_events import NULL
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
from tgbot.config import  DB_URI
from tgbot.config import load_config
from tgbot.services import broadcaster
from aiogram import Router, Bot, types
from aiogram.types import Message,FSInputFile
from tgbot.config import load_config
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State, StatesGroup
from tgbot.misc.states import getOrder, private_get
from tgbot.db import orders_update
from tgbot.keyboards.textBtn import answer_request,answer_request2

import asyncio

author2_router = Router()
config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
bot2 = Bot(token=config.tg_bot.token2, parse_mode='HTML')


async def check_id(id):
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    id = str(id)
    cur.execute('SELECT * FROM orders ')
    users = cur.fetchall()
    answer = False
    for user in users:
        if user[0] == id:
            answer = True
    cur.close()
    base.close()
    return answer

async def auf_author(id):
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    id = str(id)
    cur.execute('SELECT * FROM authors ')
    users = cur.fetchall()
    answer = False
    for user in users:
        if user[0] == id:
            answer = True
    cur.close()
    base.close()
    return answer



async def search_author(state: FSMContext, generated_id): 
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    cur.execute('SELECT * FROM authors WHERE busyness <= authors.plane_busyness ORDER BY rating DESC')
    authors = cur.fetchall()
    data = (str(generated_id),)
    cur.execute('SELECT * FROM orders WHERE id = %s', data)
    order = cur.fetchall()
    flag = False
    author_ids = ''
    btn = answer_request()
    for author in authors:
        print('start for')
        await bot2.send_message(author[0],f'''Тип роботы: {order[0][5]}
Тема работы: {order[0][7]}
Обьем работы: {order[0][6]} ст.
Контакты: @{order[0][3]}
Коментарий: {order[0][18]}
                                ''',reply_markup=btn.as_markup(resize_keyboard=True))
        await state.set_state(getOrder.answer)  
        await asyncio.sleep(10)
        try:
            data = (str(author[0]),)
            cur.execute('SELECT answer FROM authors WHERE id = %s', data)
            answer = cur.fetchall()
            if str(answer[0][0]) == 'прийняти':
                flag = True
                author_ids = author[0]
                await state.clear()
                break
        except KeyError: 
            await state.clear()
    print('end for')
    if flag == False:
        print('false')
        await orders_update.decline_order(generated_id)
        await orders_update.update_answer(NULL,str(author_ids))
        await search_private_author(generated_id)
    else:
        print('true')
        await orders_update.confirm_order(generated_id, str(author_ids))
        await orders_update.update_busyness(order[0][5], str(author_ids))
        await orders_update.update_answer(NULL,str(author_ids))
        
        
async def search_private_author(generated_id): 
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    cur.execute('SELECT * FROM authors WHERE busyness <= authors.plane_busyness and private = true ORDER BY rating DESC')
    authors = cur.fetchall()
    data = (str(generated_id),)
    cur.execute('SELECT * FROM orders WHERE id = %s', data)
    order = cur.fetchall()
    btn = answer_request2()
    for author in authors:
            await bot2.send_message(author[0],f'''Тип роботы: {order[0][5]}
Тема работы: {order[0][7]}
Обьем работы: {order[0][6]} ст.
Контакты: @{order[0][3]}
Коментарий: {order[0][18]}
                                ''',reply_markup=btn.as_markup(resize_keyboard=True))
    await asyncio.sleep(10)
    cur.execute('SELECT * FROM authors WHERE busyness <= authors.plane_busyness and private = true ORDER BY answer DESC')
    authors = cur.fetchall()
    try:
        if int(authors[0][0]) > 1:
            await orders_update.confirm_order(generated_id, str(authors[0][0]))
            await orders_update.update_price(generated_id,str(authors[0][11]))
            await orders_update.update_busyness(order[0][5], authors[0][0])
            await orders_update.update_answer(NULL,str(authors[0][0]))
    except KeyError: 
        print('err') 
    try:
        if int(authors[0][1]) > 1:
            await orders_update.confirm_sec_order(generated_id, str(authors[0][0]))
            await orders_update.update_answer(NULL,str(authors[0][0]))
    except KeyError: 
        print('err') 
    await orders_update.update_answer(NULL,str(authors[0][0]))
    
    
@author2_router.message_handler(text = ['прийняти','відхилити','прийняти замовлення'])
async def test_start(message: Message, state: FSMContext):
    if message.text == 'прийняти':
        await orders_update.update_answer('прийняти',str(message.from_user.id))
    elif message.text == 'відхилити':
        await orders_update.update_answer('відхилити',str(message.from_user.id))
    elif message.text == 'прийняти замовлення':
        await bot2.send_message(message.from_user.id,'надішліть ціну')
        await state.set_state(private_get.money)  
        
        
@author2_router.message_handler(content_types=types.ContentType.TEXT, state=private_get.money)
async def test_start(message: Message, state: FSMContext):
    await orders_update.update_answer(message.text,str(message.from_user.id))
    await state.clear()

async def get_list_of_authors():
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    cur.execute('SELECT * FROM authors ')
    users = cur.fetchall()
    answer = []
    for user in users:
        answer.append(user[0])
    cur.close()
    base.close()
    return answer

