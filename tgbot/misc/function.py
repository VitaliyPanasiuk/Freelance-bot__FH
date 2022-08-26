# from asyncio.windows_events import NULL
# from curses.ascii import NUL
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
import datetime

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
    data = (str(generated_id),)
    cur.execute('SELECT * FROM orders WHERE id = %s', data)
    order = cur.fetchall()
    cur.execute('SELECT * FROM authors WHERE busyness <= authors.plane_busyness  ORDER BY rating DESC')
    authors = cur.fetchall()
    
    flag = False
    author_ids = ''
    btn = answer_request()
    for author in authors:
        if author[7] == order[0][4]:
            await bot2.send_message(author[0],f'''id: {order[0][0]}
Вид роботи: {order[0][5]}
Тема роботи: {order[0][7]}
Обсяг роботи: {order[0][6]} ст.
Унікальність роботи: {order[0][8]}
Спеціальність: {order[0][4]}
Коментар: {order[0][18]}
Ціна: {order[0][16]}
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
    if flag == False:
        await orders_update.decline_order(generated_id)
        await orders_update.update_answer(None,str(author_ids))
        await search_private_author(generated_id)
    else:
        await orders_update.confirm_order(generated_id, str(author_ids))
        await orders_update.update_busyness(order[0][5], str(author_ids))
        await orders_update.update_answer(None,str(author_ids))
        
        
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
        await bot2.send_message(author[0],f'''id: {order[0][0]}
Вид роботи: {order[0][5]}
Тема роботи: {order[0][7]}
Обсяг роботи: {order[0][6]} ст.
Унікальність роботи: {order[0][8]}
Спеціальність: {order[0][4]}
Коментар: {order[0][18]}
Ціна: {order[0][16]}
                                ''',reply_markup=btn.as_markup(resize_keyboard=True))
    await asyncio.sleep(10)
    cur.execute('SELECT * FROM authors WHERE busyness <= authors.plane_busyness and private = true ORDER BY answer DESC')
    authors = cur.fetchall()
    try:
        if int(authors[0][0]) > 1:
            await orders_update.confirm_order(generated_id, str(authors[0][0]))
            await orders_update.update_price(generated_id,str(authors[0][11]))
            await orders_update.update_busyness(order[0][5], authors[0][0])
            await orders_update.update_answer(None,str(authors[0][0]))
    except KeyError: 
        print('err') 
    try:
        if int(authors[0][1]) > 1:
            await orders_update.confirm_sec_order(generated_id, str(authors[0][0]))
            await orders_update.update_answer(None,str(authors[0][0]))
    except KeyError: 
        print('err') 
    await orders_update.update_answer(None,str(authors[0][0]))
    
    
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
    cur.execute('SELECT * FROM authors')
    users = cur.fetchall()
    answer = []
    for user in users:
        answer.append(user[0])
    cur.close()
    base.close()
    return answer

async def alert8():
    while True:
        base = psycopg2.connect(DB_URI,sslmode="require")
        cur = base.cursor()
        cur.execute('''SELECT * FROM orders WHERE status IN ('План') and alert = true''')
        orders = cur.fetchall()
        for order in orders:
            now = datetime.datetime.now()
            time = datetime.datetime.strptime(order[12],"%d-%m-%Y %H:%M")
            text36 = datetime.timedelta(days =1, hours=12)
            text24 = datetime.timedelta(days =1)
            text48 = datetime.timedelta(days =2)
            hours24 = time + text24
            hours36 = time + text36
            hours48 = time + text48
            if now < hours48:
                await bot2.send_message(order[13],'Нагадування! До замовлення №' + str(order[0]) + ', пріоритетність — ' + str(orders[27]) + ', потрібно терміново скласти та надіслати план протягом 12год')
            elif now < hours36:
                if orders[27] < 3:
                    data = (3,str(order[0]))
                    cur.execute('UPDATE orders SET priority=%s WHERE id=%s', data)
                await bot2.send_message(order[13],'Нагадування! До замовлення №' + str(order[0]) + ', пріоритетність — ' + str(orders[27]) + ', потрібно терміново скласти та надіслати план протягом 12год')
            elif now < hours24:
                await bot2.send_message(order[13],'Нагадування! До замовлення №' + str(order[0]) + ', пріоритетність — ' + str(orders[27]) + ', потрібно скласти та надіслати план протягом 12год')
        await asyncio.sleep(43200)


async def alert12():
    while True:
        base = psycopg2.connect(DB_URI,sslmode="require")
        cur = base.cursor()
        cur.execute('''SELECT * FROM orders WHERE status IN ('В роботі') and alert = true''')
        orders = cur.fetchall()
        for order in orders:
            now = datetime.datetime.now()
            time = datetime.datetime.strptime(order[26],"%d-%m-%Y %H:%M")
            text120 = datetime.timedelta(hours=120)
            text72 = datetime.timedelta(hours=72)
            text48 = datetime.timedelta(hours=48)
            text24 = datetime.timedelta(hours=24)
            text12 = datetime.timedelta(hours=12)
            hours120 = time - text120
            hours72 = time - text72
            hours48 = time - text48
            hours24 = time - text24
            hours12 = time - text12
            if now > hours12:
                await bot2.send_message(order[13],'Нагадування! До замовлення №' + str(order[0]) + ', пріоритетність — ' + str(orders[27]) + ', дедлайн - ' + str(orders[26]) + ', потрібно ТЕРМІНОВО надіслати роботу')
            elif now > hours24 and orders[27] != '12 - 24h':
                await bot2.send_message(order[13],'Нагадування! До замовлення №' + str(order[0]) + ', пріоритетність — ' + str(orders[27]) + ', завтра дедлайн - ' + str(orders[26]))
                if orders[27] <= 4:
                    data = (5,str(order[0]))
                    cur.execute('UPDATE orders SET priority=%s WHERE id=%s', data)
                data = ('12 - 24h',str(order[0]))
                cur.execute('UPDATE orders SET com_alert=%s WHERE id=%s', data)
            elif now > hours48 and orders[27] != '12 - 48h':
                await bot2.send_message(order[13],'Нагадування! До замовлення №' + str(order[0]) + ', пріоритетність — ' + str(orders[27]) + ', дедлайн за 2 дні - ' + str(orders[26]))
                data = ('12 - 48h',str(order[0]))
                cur.execute('UPDATE orders SET com_alert=%s WHERE id=%s', data)
                if orders[27] <= 3:
                    data = (4,str(order[0]))
                    cur.execute('UPDATE orders SET priority=%s WHERE id=%s', data)
            elif now > hours72 and orders[27] != '12 - 72h':
                await bot2.send_message(order[13],'Нагадування! До замовлення №' + str(order[0]) + ', пріоритетність — ' + str(orders[27]) + ', дедлайн за 3 дні - ' + str(orders[26]))
                data = ('12 - 72h',str(order[0]))
                cur.execute('UPDATE orders SET com_alert=%s WHERE id=%s', data)
            elif now > hours120 and orders[27] != '12 - 120h':
                await bot2.send_message(order[13],'Нагадування! До замовлення №' + str(order[0]) + ', пріоритетність — ' + str(orders[27]) + ', дедлайн за 5 днів - ' + str(orders[26]))
                data = ('12 - 120h',str(order[0]))
                cur.execute('UPDATE orders SET com_alert=%s WHERE id=%s', data)
        await asyncio.sleep(43200)
        
async def alert16():
    while True:
        base = psycopg2.connect(DB_URI,sslmode="require")
        cur = base.cursor()
        cur.execute('''SELECT * FROM orders WHERE status IN ('В роботі') and alert = true''')
        orders = cur.fetchall()
        for order in orders:
            now = datetime.datetime.now()
            time = datetime.datetime.strptime(order[26],"%d-%m-%Y %H:%M")
            text120 = datetime.timedelta(hours=120)
            text72 = datetime.timedelta(hours=72)
            text48 = datetime.timedelta(hours=48)
            text24 = datetime.timedelta(hours=24)
            text12 = datetime.timedelta(hours=12)
            hours120 = time - text120
            hours72 = time - text72
            hours48 = time - text48
            hours24 = time - text24
            hours12 = time - text12
            if now > hours12:
                await bot2.send_message(order[13],'Нагадування! До замовлення №' + str(order[0]) + ', пріоритетність — ' + str(orders[27]) + ', дедлайн - ' + str(orders[26]) + ', потрібно ТЕРМІНОВО надіслати роботу')
            elif now > hours24 and orders[27] != '16 - 24h':
                await bot2.send_message(order[13],'Нагадування! До замовлення №' + str(order[0]) + ', пріоритетність — ' + str(orders[27]) + ', дедлайн на внесення правок за 1 день - ' + str(orders[26]))
                if orders[27] <= 4:
                    data = (5,str(order[0]))
                    cur.execute('UPDATE orders SET priority=%s WHERE id=%s', data)
                data = ('16 - 24h',str(order[0]))
                cur.execute('UPDATE orders SET com_alert=%s WHERE id=%s', data)
            elif now > hours48 and orders[27] != '16 - 48h':
                await bot2.send_message(order[13],'Нагадування! До замовлення №' + str(order[0]) + ', пріоритетність — ' + str(orders[27]) + ', дедлайн на внесення правок за 2 дні - ' + str(orders[26]))
                data = ('16 - 48h',str(order[0]))
                cur.execute('UPDATE orders SET com_alert=%s WHERE id=%s', data)
                if orders[27] <= 3:
                    data = (4,str(order[0]))
                    cur.execute('UPDATE orders SET priority=%s WHERE id=%s', data)
            elif now > hours72 and orders[27] != '16 - 72h':
                await bot2.send_message(order[13],'Нагадування! До замовлення №' + str(order[0]) + ', пріоритетність — ' + str(orders[27]) + ', дедлайн на внесення правок за 3 дні - ' + str(orders[26]))
                data = ('16 - 72h',str(order[0]))
                cur.execute('UPDATE orders SET com_alert=%s WHERE id=%s', data)
            elif now > hours120 and orders[27] != '16 - 120h':
                await bot2.send_message(order[13],'Нагадування! До замовлення №' + str(order[0]) + ', пріоритетність — ' + str(orders[27]) + ', дедлайн на внесення правок за 5 днів - ' + str(orders[26]))
                data = ('16 - 120h',str(order[0]))
                cur.execute('UPDATE orders SET com_alert=%s WHERE id=%s', data)
        await asyncio.sleep(43200)
            
                
                    

