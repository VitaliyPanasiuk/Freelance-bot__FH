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

from tgbot.misc.states import getOrder
from tgbot.misc.function import check_id, search_author

from tgbot.keyboards.textBtn import typeBtn

from tgbot.db import orders_update
import asyncio



user_router = Router()
config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
bot2 = Bot(token=config.tg_bot.token2, parse_mode='HTML')

    
@user_router.message(commands=["start"])
async def user_start(message: Message, state: FSMContext):
    userid = message.from_user.id
    btn = typeBtn()
    await bot.send_message(userid,"Привіт! Я кролик, який з радістю допоможе тобі. Для оцінки вартості дай відповідь лише на 4 питання, гаразд?")
    await bot.send_message(userid,"Який вид роботи тебе цікавить?",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(getOrder.type)   
    


@user_router.message_handler(content_types=types.ContentType.TEXT, state=getOrder.type)
async def typeOfOrder(message: types.Message, state: FSMContext):
    userid = message.from_user.id
    userName = message.from_user.username
    answer = message.text
    if answer == 'Інше':
        await state.set_state(getOrder.new_type) 
    else:
        await state.update_data(type=answer) 
        await state.update_data(username=userName) 
        await bot.send_message(userid,"Яка у тебе тема?", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(getOrder.topic)   
        
@user_router.message_handler(content_types=types.ContentType.TEXT, state=getOrder.type)
async def typeOfOrder(message: types.Message, state: FSMContext):
    userid = message.from_user.id
    userName = message.from_user.username
    answer = message.text
    await state.update_data(type=answer) 
    await state.update_data(username=userName) 
    await bot.send_message(userid,"Яка у тебе тема?", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(getOrder.topic)   
    
    
@user_router.message_handler(content_types=types.ContentType.TEXT, state = getOrder.topic)
async def typeOfOrder(message: types.Message, state: FSMContext):
    userid = message.from_user.id
    answer = message.text
    await state.update_data(topic=answer) 
    await bot.send_message(userid,"Зрозумів, а який обсяг має бути? Вкажи кількість сторінок.", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(getOrder.pages)   
    
    
@user_router.message_handler(content_types=types.ContentType.TEXT, state = getOrder.pages)
async def typeOfOrder(message: types.Message, state: FSMContext):
    userid = message.from_user.id
    answer = message.text
    await state.update_data(pages=int(answer)) 
    await bot.send_message(userid,"І останнє питання, коли у тебе дедлайн?", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(getOrder.comment)   
    
@user_router.message_handler(content_types=types.ContentType.TEXT, state = getOrder.comment)
async def typeOfOrder(message: types.Message, state: FSMContext):
    userid = message.from_user.id
    answer = message.text
    
    await state.update_data(comment=answer) 
    order_data = await state.get_data()
    
    generated_id = ''
    test = randint(0,1000000)
    generated_id = str(test)
    if await check_id(generated_id):
        while await check_id(generated_id):
            test = randint(0,1000000)
            generated_id = str(test)
    now = datetime.datetime.now()
    time = now.strftime("%d-%m-%Y %H:%M")
    await orders_update.reg_order(generated_id,time,order_data['username'],order_data['comment'],order_data['pages'],order_data['topic'],order_data['type'])
    await state.clear()
    await bot.send_message(userid,"Супер! Я вже передаю твою інформацію нашому менеджеру. Він зв’яжеться з тобою найближчим часом. Гарного дня :)", reply_markup=types.ReplyKeyboardRemove())
    await orders_update.new_order(generated_id)
    

    
    
    
    
    