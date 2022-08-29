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




@admin_router.message(commands=["mailing"])
async def admin_start(message: Message, state: FSMContext):
    # await message.reply("Отправьте id тимлида!")
    # await state.set_state(mailing.get_teamlead)
    await message.reply("Отправьте сообщение которое хотите разослать всем пользователям!")
    await state.set_state(mailing.get_answer)
    
@admin_router.message(content_types=types.ContentType.TEXT, state=mailing.get_teamlead)
async def admin_start(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(get_teamlead=text) 
    await message.reply("Отправьте сообщение которое хотите разослать всем пользователям!")
    await state.set_state(mailing.get_answer)
    
    
@admin_router.message(content_types=types.ContentType.TEXT, state=mailing.get_answer)
async def admin_start(message: Message, state: FSMContext):
    text = message.text
    user_id = message.from_user.id
    list_of_users = await get_list_of_authors(user_id)
    
    if list_of_users:
        for i in list_of_users:
            await bot2.send_message(i,text)
    else:
        await bot2.send_message(message.from_user.id,"Пользователей не найдено")
        
    await bot2.send_message(message.from_user.id,"Сообщение было разослано всем пользователям")
    await state.clear()
    
@admin_router.message(commands=["addauthor"])
async def admin_start(message: Message, state: FSMContext):
    await message.reply("Отправьте id автора!")
    await state.set_state(mailing.get_author)
    
@admin_router.message(content_types=types.ContentType.TEXT, state=mailing.get_author)
async def admin_start(message: Message, state: FSMContext):
    
    text = message.text
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    data = (str(text),)
    cur.execute('INSERT INTO authors_ids (authors_id)  VALUES (%s)', data)
    
    base.commit()
    cur.close()
    base.close()
    
@admin_router.message(commands=["addauthorprivate"])
async def admin_start(message: Message, state: FSMContext):
    await message.reply("Отправьте id автора!")
    await state.set_state(mailing.get_author_private)
    
    
@admin_router.message(content_types=types.ContentType.TEXT, state=mailing.get_author_private)
async def admin_start(message: Message, state: FSMContext):
    
    text = message.text
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    data = (str(text),)
    cur.execute('UPDATE authors SET private = true WHERE id=%s', data)
    
    base.commit()
    cur.close()
    
    base.close()
@admin_router.message(commands=["search_author"])
async def admin_start(message: Message, state: FSMContext):
    await message.reply("Отправьте id заказа!")
    await state.set_state(mailing.get_order_id)
    
@admin_router.message(content_types=types.ContentType.TEXT, state=mailing.get_order_id)
async def admin_start(message: Message, state: FSMContext):
    text = message.text
    await search_author(str(text))
    
    

