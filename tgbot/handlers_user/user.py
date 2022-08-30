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

from pipedrive.client import Client
import json



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
        await bot.send_message(userid,"Опиши свій вид роботи.", reply_markup=types.ReplyKeyboardRemove()) 
        await state.set_state(getOrder.new_type)
    else:
        await state.update_data(type=answer) 
        await state.update_data(username=userName) 
        await bot.send_message(userid,"Яка у тебе тема?", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(getOrder.topic)  

@user_router.message_handler(content_types=types.ContentType.TEXT, state=getOrder.new_type)
async def typeOfOrder(message: types.Message, state: FSMContext):
    userid = message.from_user.id
    userName = message.from_user.username
    answer = message.text
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
    await state.update_data(pages=answer) 
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
    
    await bot.send_message(userid,"Супер! Я вже передаю твою інформацію нашому менеджеру. Він зв’яжеться з тобою найближчим часом. Гарного дня :)", reply_markup=types.ReplyKeyboardRemove())
    await orders_update.new_order(generated_id)
    client = Client(domain='https://bunny2.pipedrive.com/')
    client.set_api_token('83b3829fdfc9028b7bf80a419f7d77cb4c217742')
    data = {'328c4d26267c3f44b8f41f8d525127fc119bae6f': generated_id,
            '02858634b27afa9b3781ea8f4d144b223f1cdd70': time,
            'deba793a0a82282ed6ee931b4ccb1f1a5f7d11d0': order_data['username'],
            '6b4cb9ad4eaf8a8c2b388d22f8c6a2d2a723d512': order_data['comment'],
            'd88cd8ea3b3453d111296b960ed6205acbf75094': order_data['pages'],
            '8a85577eeb5ffff5a1dc3871c77b103b26b7fbf3': order_data['topic'],
            'title': order_data['type']}
    response = client.deals.create_deal(data) 
    await state.clear()
    

    
    
    
    
    