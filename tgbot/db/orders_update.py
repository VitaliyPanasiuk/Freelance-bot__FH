import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
from tgbot.config import  DB_URI



async def reg_order(sub_id ,time, username,comment,pages,topic,type):
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    data = (sub_id, time, username, type, pages,topic,False,comment)
    cur.execute('INSERT INTO orders (sub_id, date, social, type, pages, topic, costs_status, comment)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s)', data)
    
    base.commit()
    cur.close()
    base.close()
    
async def reg_order_crm(sub_id ,time, username,comment,pages,topic,type):
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    data = (sub_id, time, username, type, pages,topic,comment)
    cur.execute('INSERT INTO orders (sub_id, date, social, type, pages, topic, comment)  VALUES (%s,%s,%s,%s,%s,%s,%s)', data)
    
    base.commit()
    cur.close()
    base.close()
    
async def reg_author(id,card,speciality):
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    data = (id,card,speciality)
    cur.execute('INSERT INTO authors (id,card,speciality)  VALUES (%s,%s,%s)', data)
    
    base.commit()
    cur.close()
    base.close()
    
    
async def confirm_order(order_id,author_id):
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    data = (str(author_id),str(order_id))
    cur.execute('UPDATE orders SET author_id=%s WHERE id=%s', data)
    
    base.commit()
    cur.close()
    base.close()
    
async def confirm_sec_order(order_id,author_id):
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    data = (str(author_id),str(order_id))
    cur.execute('UPDATE orders SET sec_author=%s WHERE id=%s', data)
    
    base.commit()
    cur.close()
    base.close()
    
async def update_price(order_id,price):
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    data = (str(price),str(order_id))
    cur.execute('UPDATE orders SET costs=%s WHERE id=%s', data)
    
    base.commit()
    cur.close()
    base.close()
async def update_sec_price(order_id,price):
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    data = (str(price),str(order_id))
    cur.execute('UPDATE orders SET sec_costs=%s WHERE id=%s', data)
    
    base.commit()
    cur.close()
    base.close()
    
async def decline_order(order_id):
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    data = ('Дізнатись ціну',str(order_id))
    cur.execute('UPDATE orders SET status = %s WHERE id=%s', data)
    
    base.commit()
    cur.close()
    base.close()
    
async def new_order(order_id):
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    data = ('Знайти автора',str(order_id))
    cur.execute('UPDATE orders SET status = %s WHERE id=%s', data)
    
    base.commit()
    cur.close()
    base.close()
    
async def update_answer(answer,author_id):
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    data = (answer,str(author_id))
    cur.execute('UPDATE authors SET answer = %s WHERE id=%s', data)
    
    base.commit()
    cur.close()
    base.close()
    
async def update_busyness(answer,author_id):
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    
    if answer == 'Ece':
        data = (0.3,str(author_id))
    elif answer == 'Тези':
        data = (0.5,str(author_id))
    elif answer == 'Реферат':
        data = (0.5,str(author_id))
    elif answer == 'Практичне завдання':
        data = (1,str(author_id))
    elif answer == 'Презентація':
        data = (0.3,str(author_id))
    elif answer == 'Курсова':
        data = (1,str(author_id))
    elif answer == 'Дипломна':
        data = (1.5,str(author_id))
    elif answer == 'Магістерська':
        data = (2,str(author_id))
    else:
        data = (0.1,str(author_id))
    cur.execute('UPDATE authors SET busyness = busyness + %s WHERE id=%s', data)
    
    base.commit()
    cur.close()
    base.close()
    
