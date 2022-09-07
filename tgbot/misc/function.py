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
from random import randint

from pipedrive.client import Client
import json


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



async def search_author(generated_id): 
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
    flag_for = False
    for author in authors:
        if order[0][5] in author[7]:
            money = 0
            costs = order[0][15].split(',')
            money += int(costs[0])
            money += int(costs[1])
            await bot2.send_message(author[0],f'''
🟢 НОВЕ ЗАМОВЛЕННЯ 🟢

🆔: {order[0][1]}
◾️ Спеціальність: {order[0][5]}
◽️ Вид роботи: {order[0][6]}
◾️ Тема: {order[0][8]}
◽️ Обсяг: {order[0][7]} ст.
◾️ Унікальність: {order[0][9]}
◽️ Дедлайн: {order[0][27]}
◾️ Коментар: {order[0][19]}
💸 Ціна: {money}
            ''',reply_markup=btn.as_markup(resize_keyboard=True))
            await asyncio.sleep(300)
            cur.execute('SELECT * FROM authors WHERE busyness <= authors.plane_busyness  ORDER BY rating DESC')
            authors = cur.fetchall()
            
            for author in authors:
                if author[11] == 'прийняти':
                    flag_for = True
                    flag = True
                    author_ids = str(author[0])
                    break
        if flag_for:
            break
    for author in authors:
            await orders_update.update_answer(None,str(author[0]))    
    if flag == False:
        await orders_update.decline_order(generated_id)
        await search_private_author(generated_id)
    else:
        await bot2.send_message(str(author_ids),f'Чудово, замовлення твоє! Якщо виникнуть питання, ти завжди можеш написати менеджеру😉\n🆔: {order[0][1]}')
        await orders_update.confirm_order(generated_id, str(author_ids))
        await orders_update.update_busyness(order[0][5], str(author_ids))
    cur.close()
    base.close()    
    


        
# async def search_author(generated_id): 
#     base = psycopg2.connect(DB_URI,sslmode="require")
#     cur = base.cursor()
#     data = (str(generated_id),)
#     cur.execute('SELECT * FROM orders WHERE id = %s', data)
#     order = cur.fetchall()
#     cur.execute('SELECT * FROM authors WHERE busyness <= authors.plane_busyness  ORDER BY rating DESC')
#     authors = cur.fetchall()
#     print(authors)
#     flag = False
#     author_ids = ''
#     btn = answer_request()
#     for author in authors:
#         print(author[7])
#         print(order[0][4])
#         if order[0][4] in author[7]:
#             money = 0
#             costs = order[0][16].split(',')
#             money += int(costs[0])
#             money += int(costs[1])
#             await bot2.send_message(author[0],f'''
# 🟢 НОВЕ ЗАМОВЛЕННЯ 🟢

# 🆔: {order[0][1]}
# ◾️ Спеціальність: {order[0][4]}
# ◽️ Вид роботи: {order[0][5]}
# ◾️ Тема: {order[0][7]}
# ◽️ Обсяг: {order[0][6]} ст.
# ◾️ Унікальність: {order[0][8]}
# ◽️ Дедлайн: {order[0][26]}
# ◾️ Коментар: {order[0][18]}
# 💸 Ціна: {money}
#                                     ''',reply_markup=btn.as_markup(resize_keyboard=True))
#             # await state.set_state(getOrder.answer)  
#             await asyncio.sleep(300)
#             try:
#                 data = (str(author[0]),)
#                 cur.execute('SELECT answer FROM authors WHERE id = %s', data)
#                 answer = cur.fetchall()
#                 if str(answer[0][0]) == 'прийняти':
#                     flag = True
#                     author_ids = author[0]
#                     # await state.clear()
#                     break
#             except BaseException : 
#                 # await state.clear()
#                 print(BaseException)
#     if flag == False:
#         await orders_update.decline_order(generated_id)
#         await orders_update.update_answer(None,str(author_ids))
#         await bot2.send_message(str(author_ids),'Чудово, замовлення твоє! Якщо виникнуть питання, ти завжди можеш написати менеджеру😉\n🆔: {order[0][1]}')
#         await search_private_author(generated_id)
#     else:
#         await orders_update.confirm_order(generated_id, str(author_ids))
#         await orders_update.update_busyness(order[0][5], str(author_ids))
#         await orders_update.update_answer(None,str(author_ids))
        
        
async def search_private_author(generated_id): 
    print('start_private')
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    cur.execute('SELECT * FROM authors WHERE busyness <= authors.plane_busyness and private = true ORDER BY rating DESC')
    authors = cur.fetchall()
    data = (str(generated_id),)
    cur.execute('SELECT * FROM orders WHERE id = %s', data)
    order = cur.fetchall()
    btn = answer_request2()
    for author in authors:
        await bot2.send_message(author[0],f'''
🟡АУКЦОН🟡

🆔: {order[0][1]}
◾️ Спеціальність: {order[0][5]}
◽️ Вид роботи: {order[0][6]}
◾️ Тема: {order[0][8]}
◽️ Обсяг {order[0][7]} ст.
◾️ Унікальність: {order[0][9]}
◽️ Дедлайн: {order[0][27]}
◾️ Коментар: {order[0][19]}
                                ''',reply_markup=btn.as_markup(resize_keyboard=True))
    await asyncio.sleep(7200)
    cur.execute('SELECT * FROM authors WHERE busyness <= authors.plane_busyness and private = true ORDER BY answer')
    authors = cur.fetchall()
    if len(authors) >= 1:
        if authors[0][11]:
            if authors[0][11].isdigit():
                # if authors[0][0]:
                if int(authors[0][0]) > 1:
                    money = int(authors[0][11]) / 2
                    await orders_update.confirm_order(generated_id, str(authors[0][0]))
                    price = str(money)+ ',' + str(money)
                    await orders_update.update_price(generated_id,price)
                    await orders_update.update_busyness(order[0][5], authors[0][0])
                    await orders_update.update_answer(None,str(authors[0][0]))
                    await bot2.send_message(str(authors[0][0]),'😎Твоя ставка до замовлення ID ' + str(order[0][1]) + ' перемогла! Менеджер зв`яжеться з тобою в скорому часу.')
                await orders_update.update_answer(None,str(authors[0][0]))
    if len(authors) >= 2:
        if authors[1][11]:
            if authors[1][11].isdigit():
                # if authors[1][0]:
                if int(authors[1][0]) > 1:
                    money = int(authors[1][11]) / 2
                    await orders_update.confirm_sec_order(generated_id, str(authors[1][0]))
                    await orders_update.update_answer(None,str(authors[1][0]))
                    await orders_update.update_sec_price(generated_id,str(money)+ ',' + str(money))
                await orders_update.update_answer(None,str(authors[1][0]))
    cur.close()
    base.close()    
    
# text = ['прийняти','відхилити','прийняти замовлення']
@author2_router.message_handler()
async def test_start(message: Message, state: FSMContext):
    print('handle in taken')
    auf_status = await auf_author(str(message.from_user.id))
    
    if message.text == '✅Прийняти':
        await orders_update.update_answer('прийняти',str(message.from_user.id))
    elif message.text == '❌Відхилити':
        await orders_update.update_answer('відхилити',str(message.from_user.id))
    elif message.text == '✅Прийняти замовлення':
        await bot2.send_message(message.from_user.id,'👇Вкажи свою ставку (лише число, без "грн")')
        await state.set_state(private_get.money)  
    elif message.text.isdigit() and auf_status:
        await message.reply("⚖️Ставку прийнято! Ти отримаєш сповіщення, якщо твоя ставка виграє.")
        await orders_update.update_answer(message.text,str(message.from_user.id))
    

async def get_list_of_authors(teamlead):
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    data = (str(teamlead),)
    cur.execute('SELECT * FROM authors WHERE teamlead = %s',data)
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
            time = datetime.datetime.strptime(order[13],"%d-%m-%Y %H:%M")
            text36 = datetime.timedelta(days =1, hours=12)
            text24 = datetime.timedelta(days =1)
            text48 = datetime.timedelta(days =2)
            hours24 = time + text24
            hours36 = time + text36
            hours48 = time + text48
            if now < hours48:
                await bot2.send_message(order[14],'Нагадування! До замовлення №' + str(order[1]) + ', пріоритетність — ' + str(orders[28]) + ', потрібно терміново скласти та надіслати план протягом 12год')
            elif now < hours36:
                if orders[28] < 3:
                    data = (3,str(order[0]))
                    cur.execute('UPDATE orders SET priority=%s WHERE id=%s', data)
                await bot2.send_message(order[14],'Нагадування! До замовлення №' + str(order[1]) + ', пріоритетність — ' + str(orders[28]) + ', потрібно терміново скласти та надіслати план протягом 12год')
            elif now < hours24:
                await bot2.send_message(order[14],'Нагадування! До замовлення №' + str(order[1]) + ', пріоритетність — ' + str(orders[28]) + ', потрібно скласти та надіслати план протягом 12год')
        await asyncio.sleep(43200)
        cur.close()
        base.close()

async def alert12():
    while True:
        base = psycopg2.connect(DB_URI,sslmode="require")
        cur = base.cursor()
        cur.execute('''SELECT * FROM orders WHERE status IN ('В роботі') and alert = true''')
        orders = cur.fetchall()
        for order in orders:
            now = datetime.datetime.now()
            time = datetime.datetime.strptime(order[27],"%d-%m-%Y %H:%M")
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
                await bot2.send_message(order[14],'Нагадування! До замовлення №' + str(order[1]) + ', пріоритетність — ' + str(orders[28]) + ', дедлайн - ' + str(orders[27]) + ', потрібно ТЕРМІНОВО надіслати роботу')
            elif now > hours24 and orders[29] != '12 - 24h':
                await bot2.send_message(order[14],'Нагадування! До замовлення №' + str(order[1]) + ', пріоритетність — ' + str(orders[28]) + ', завтра дедлайн - ' + str(orders[27]))
                if orders[28] <= 4:
                    data = (5,str(order[0]))
                    cur.execute('UPDATE orders SET priority=%s WHERE id=%s', data)
                data = ('12 - 24h',str(order[0]))
                cur.execute('UPDATE orders SET com_alert=%s WHERE id=%s', data)
            elif now > hours48 and orders[29] != '12 - 48h':
                await bot2.send_message(order[14],'Нагадування! До замовлення №' + str(order[1]) + ', пріоритетність — ' + str(orders[28]) + ', дедлайн за 2 дні - ' + str(orders[27]))
                data = ('12 - 48h',str(order[0]))
                cur.execute('UPDATE orders SET com_alert=%s WHERE id=%s', data)
                if orders[28] <= 3:
                    data = (4,str(order[0]))
                    cur.execute('UPDATE orders SET priority=%s WHERE id=%s', data)
            elif now > hours72 and orders[29] != '12 - 72h':
                await bot2.send_message(order[14],'Нагадування! До замовлення №' + str(order[1]) + ', пріоритетність — ' + str(orders[28]) + ', дедлайн за 3 дні - ' + str(orders[27]))
                data = ('12 - 72h',str(order[0]))
                cur.execute('UPDATE orders SET com_alert=%s WHERE id=%s', data)
            elif now > hours120 and orders[29] != '12 - 120h':
                await bot2.send_message(order[14],'Нагадування! До замовлення №' + str(order[1]) + ', пріоритетність — ' + str(orders[28]) + ', дедлайн за 5 днів - ' + str(orders[27]))
                data = ('12 - 120h',str(order[0]))
                cur.execute('UPDATE orders SET com_alert=%s WHERE id=%s', data)
        cur.close()
        base.close()
        await asyncio.sleep(43200)
        
async def alert16():
    while True:
        base = psycopg2.connect(DB_URI,sslmode="require")
        cur = base.cursor()
        cur.execute('''SELECT * FROM orders WHERE status IN ('В роботі') and alert = true''')
        orders = cur.fetchall()
        for order in orders:
            now = datetime.datetime.now()
            time = datetime.datetime.strptime(order[27],"%d-%m-%Y %H:%M")
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
                await bot2.send_message(order[14],'Нагадування! До замовлення №' + str(order[1]) + ', пріоритетність — ' + str(orders[28]) + ', дедлайн - ' + str(orders[27]) + ', потрібно ТЕРМІНОВО надіслати роботу')
            elif now > hours24 and orders[29] != '16 - 24h':
                await bot2.send_message(order[14],'Нагадування! До замовлення №' + str(order[1]) + ', пріоритетність — ' + str(orders[28]) + ', дедлайн на внесення правок за 1 день - ' + str(orders[27]))
                if orders[28] <= 4:
                    data = (5,str(order[0]))
                    cur.execute('UPDATE orders SET priority=%s WHERE id=%s', data)
                data = ('16 - 24h',str(order[0]))
                cur.execute('UPDATE orders SET com_alert=%s WHERE id=%s', data)
            elif now > hours48 and orders[29] != '16 - 48h':
                await bot2.send_message(order[14],'Нагадування! До замовлення №' + str(order[1]) + ', пріоритетність — ' + str(orders[28]) + ', дедлайн на внесення правок за 2 дні - ' + str(orders[27]))
                data = ('16 - 48h',str(order[0]))
                cur.execute('UPDATE orders SET com_alert=%s WHERE id=%s', data)
                if orders[28] <= 3:
                    data = (4,str(order[0]))
                    cur.execute('UPDATE orders SET priority=%s WHERE id=%s', data)
            elif now > hours72 and orders[29] != '16 - 72h':
                await bot2.send_message(order[14],'Нагадування! До замовлення №' + str(order[1]) + ', пріоритетність — ' + str(orders[28]) + ', дедлайн на внесення правок за 3 дні - ' + str(orders[27]))
                data = ('16 - 72h',str(order[0]))
                cur.execute('UPDATE orders SET com_alert=%s WHERE id=%s', data)
            elif now > hours120 and orders[29] != '16 - 120h':
                await bot2.send_message(order[14],'Нагадування! До замовлення №' + str(order[1]) + ', пріоритетність — ' + str(orders[28]) + ', дедлайн на внесення правок за 5 днів - ' + str(orders[27]))
                data = ('16 - 120h',str(order[0]))
                cur.execute('UPDATE orders SET com_alert=%s WHERE id=%s', data)
        cur.close()
        base.close()
        await asyncio.sleep(43200)
            
async def start_search():
    while True:
        print('start_search')
        base = psycopg2.connect(DB_URI,sslmode="require")
        cur = base.cursor()
        cur.execute('''SELECT * FROM orders WHERE status IN ('Знайти автора')''')
        orders = cur.fetchall()
        if orders:
            await search_author(str(orders[0][0]))
        cur.execute('''SELECT * FROM orders WHERE status IN ('Дізнатись ціну')''')
        orders = cur.fetchall() 
        if orders:
            await search_private_author(str(orders[0][0]))
        cur.close()
        base.close()
        await asyncio.sleep(100)
        
async def genid_crm():
    while True:
        client = Client(domain='https://bunny2.pipedrive.com/')
        client.set_api_token('83b3829fdfc9028b7bf80a419f7d77cb4c217742')
        response = client.deals.get_all_deals()
        print('getted crm db')
        for deal in response['data']:
            if deal['328c4d26267c3f44b8f41f8d525127fc119bae6f']:
                pass
            else:
                generated_id = ''
                test = randint(0,1000000)
                generated_id = str(test)
                if await check_id(generated_id):
                    while await check_id(generated_id):
                        test = randint(0,1000000)
                        generated_id = str(test) 
                data = {'328c4d26267c3f44b8f41f8d525127fc119bae6f': generated_id}
                response = client.deals.update_deal(deal['id'], data)  
                await orders_update.reg_order_crm(generated_id,deal['02858634b27afa9b3781ea8f4d144b223f1cdd70'],deal['deba793a0a82282ed6ee931b4ccb1f1a5f7d11d0'],deal['6b4cb9ad4eaf8a8c2b388d22f8c6a2d2a723d512'],deal['d88cd8ea3b3453d111296b960ed6205acbf75094'],deal['8a85577eeb5ffff5a1dc3871c77b103b26b7fbf3'],deal['title'])
        await asyncio.sleep(15)        

