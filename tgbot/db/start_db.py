import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
from tgbot.config import  DB_URI


async def postgre_start():
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    if base:
        print('data base connect Ok!')
    cur.execute('''CREATE TABLE IF NOT EXISTS authors
        (
            id             varchar(20) not null
                primary key,
            full_name      text,
            contact        text,
            rating         integer,
            busyness       numeric,
            plane_busyness integer,
            card           varchar(45),
            speciality     text,
            comment        text,
            uniqueness     integer,
            teamlead       text,
            answer         text,
            private        boolean default false,
            authors_ids    integer
        )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS orders
        (
            id            serial
                primary key,
            sub_id        varchar(20),
            source        varchar(20),
            date          text,
            social        text,
            speciality    text,
            type          varchar(45),
            pages         text,
            topic         text,
            uniqueness    text,
            real_deadline text,
            files         text,
            status        text,
            fix_date      text,
            author_id     text
                references authors,
            price         integer,
            price_status  text,
            costs         text,
            costs_status  text,
            comment       text,
            teamlead      text,
            date_end      text,
            response      text,
            city          text,
            uni           text,
            faculty       text,
            sec_author    text,
            fact_deadline text,
            priority      integer default 1,
            com_alert     text    default 0,
            alert         boolean,
            sec_costs     text,
            coeff         numeric,
            author_name   text
        )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS admins
        (
            id       serial
                primary key,
            admin_id text
        )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS authors_ids
        (
            id         serial
                primary key,
            authors_id text
        )''')
    
    base.commit()
    cur.close()
    base.close()
    