import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
from tgbot.config import  DB_URI


async def postgre_start():
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    if base:
        print('data base connect Ok!')
    cur.execute('''CREATE TABLE IF NOT EXISTS orders(
        id varchar(20) primary key,
        source varchar(20),
        date text,
        social text,
        speciality text,
        type varchar(15),
        pages int,
        topic text,
        uniqueness int,
        deadline text,
        files text,
        status text,
        date_take text,
        author_id text,
        price int,
        price_status boolean,
        costs int,
        costs_status boolean,
        coment text,
        teamlead text,
        date_end text,
        response text,
        city text,
        uni text,
        faculty text
        )''')
    
    base.commit()
    cur.close()
    base.close()
    