from aiogram import Router
from aiogram import Router, Bot, types
from aiogram.types import Message,FSInputFile

from tgbot.config import load_config

from tgbot.filters.admin import AdminFilter

from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State, StatesGroup

from tgbot.misc.states import mailing,reg_author
from tgbot.misc.function import get_list_of_authors
from tgbot.misc.function import check_id, search_author
from tgbot.keyboards.inline import adm_buttons
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
from tgbot.config import  DB_URI

import asyncio


admin_router = Router()
admin_router.message.filter(AdminFilter())
config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
bot2 = Bot(token=config.tg_bot.token2, parse_mode='HTML')



@admin_router.message(commands=["start"])
async def admin_start(message: Message, state: FSMContext):
    btn = adm_buttons()
    await message.reply("Здравствуй админ!",reply_markup=btn.as_markup())
    
@admin_router.callback_query(lambda c: c.data == "mailing")
async def admin_start(callback_query: types.CallbackQuery, state: FSMContext):
    # await message.reply("Отправьте id тимлида!")
    # await state.set_state(mailing.get_teamlead)]
    userid = callback_query.from_user.id
    await bot2.send_message(userid, "Отправьте сообщение которое хотите разослать пользователям!")
    await state.set_state(mailing.get_answer)
    
# @admin_router.message(content_types=types.ContentType.TEXT, state=mailing.get_teamlead)
# async def admin_start(message: Message, state: FSMContext):
#     text = message.text
#     await state.update_data(get_teamlead=text) 
#     await message.reply("Отправьте сообщение которое хотите разослать всем пользователям!")
#     await state.set_state(mailing.get_answer)
    
    
@admin_router.message(content_types=types.ContentType.TEXT, state=mailing.get_answer)
async def admin_start(callback_query: types.CallbackQuery, state: FSMContext):
    text = callback_query.text
    user_id = callback_query.from_user.id
    list_of_users = await get_list_of_authors(user_id)
    
    if list_of_users:
        for i in list_of_users:
            await bot2.send_message(i,text)
    else:
        await bot2.send_message(user_id,"Пользователей не найдено")
        
    await bot2.send_message(user_id,"Сообщение было разослано всем пользователям")
    await state.clear()
    
@admin_router.callback_query(lambda c: c.data == "addauthor")
async def admin_start(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    await bot2.send_message(user_id,"Отправьте id автора!")
    await state.set_state(mailing.get_author)
    
@admin_router.message(content_types=types.ContentType.TEXT, state=mailing.get_author)
async def admin_start(message: Message, state: FSMContext):
    
    text = message.text
    base = psycopg2.connect(
        dbname=config.db.database,
        user=config.db.user,
        password=config.db.password,
        host=config.db.host,)
    cur = base.cursor()
    data = (str(text),)
    cur.execute('INSERT INTO authors_ids (authors_id)  VALUES (%s)', data)
    
    base.commit()
    cur.close()
    base.close()
    
@admin_router.callback_query(lambda c: c.data == "addauthorprivate")
async def admin_start(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    await bot2.send_message(user_id,"Отправьте id автора!")
    await state.set_state(mailing.get_author_private)
    
    
@admin_router.message(content_types=types.ContentType.TEXT, state=mailing.get_author_private)
async def admin_start(message: Message, state: FSMContext):
    
    text = message.text
    base = psycopg2.connect(
        dbname=config.db.database,
        user=config.db.user,
        password=config.db.password,
        host=config.db.host,)
    cur = base.cursor()
    data = (str(text),)
    cur.execute('UPDATE authors SET private = true WHERE id=%s', data)
    
    base.commit()
    cur.close()
    
    base.close()
# @admin_router.message(commands=["search_author"])
# async def admin_start(message: Message, state: FSMContext):
#     await message.reply("Отправьте id заказа!")
#     await state.set_state(mailing.get_order_id)
    
# @admin_router.message(content_types=types.ContentType.TEXT, state=mailing.get_order_id)
# async def admin_start(message: Message, state: FSMContext):
#     text = message.text
#     await search_author(str(text))
 

@admin_router.callback_query(lambda c: c.data == "authorslist")
async def admin_start(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    base = psycopg2.connect(
        dbname=config.db.database,
        user=config.db.user,
        password=config.db.password,
        host=config.db.host,)
    cur = base.cursor()
    data1 = (str(user_id),)
    cur.execute('''SELECT * FROM authors WHERE teamlead = %s''',data1)
    authors = cur.fetchall()
    last_message = ''
    total_earn = 0
    for author in authors:
        data = (author[0],)
        cur.execute('''SELECT * FROM orders WHERE author_id = %s''',data)
        orders = cur.fetchall()
        amount_orders = 0
        earn_orders = 0
        for order in orders:
            costs = order[17].split(',')
            cost_status = order[18].split(',')
            if cost_status[0] == 'false' and cost_status[1] == 'false':
                amount_orders += 1
                earn_orders += float(costs[0]) 
            elif cost_status[0] == 'true' and cost_status[1] == 'false':
                earn_orders += float(costs[0]) 
        a = float('{:.1f}'.format(earn_orders))
        last_message += author[0] + ', ' + author[1] + ', ' + str(amount_orders) + ', ' + str(a) + ', ' + author[6] + '\n'
        total_earn += earn_orders
    last_message += 'Сума = ' + str(total_earn)
    await bot2.send_message(user_id, last_message)
    cur.close()
    base.close() 