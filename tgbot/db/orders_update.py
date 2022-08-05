import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
from tgbot.config import  DB_URI


async def reg_order(id,time, username,comment,pages,topic,type):
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    data = (id, time, username, type, pages,topic,comment)
    cur.execute('INSERT INTO orders (id, date, social, type, pages,topic,comment)  VALUES (%s,%s,%s,%s,%s,%s,%s)', data)
    
    base.commit()
    cur.close()
    base.close()