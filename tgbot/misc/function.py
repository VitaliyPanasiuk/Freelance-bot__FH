import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
from tgbot.config import  DB_URI
from tgbot.config import load_config
from tgbot.services import broadcaster
from aiogram import Bot, Dispatcher

config = load_config(".env")

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