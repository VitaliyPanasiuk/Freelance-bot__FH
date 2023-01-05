from dataclasses import dataclass

from environs import Env
import os

DB_URI = 'postgres://dcnfirqzrwytme:c4c56dad1312454198e059036ee2a0747b05b4cbc1cef3f9133e1f31b78388ba@ec2-34-202-5-87.compute-1.amazonaws.com:5432/d4fqto9tiii03i'
import psycopg2
from psycopg2 import sql

def get_admins():
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    admins = []
    try:
        cur.execute('''select * from admins''')
        rows = cur.fetchall()
        for i in rows:
            admins.append(i[1])
    except:
        admins.append('1')
    cur.close()
    base.close()
    return admins

def get_authors():
    base = psycopg2.connect(DB_URI,sslmode="require")
    cur = base.cursor()
    authors = []
    try:
        cur.execute('''select * from authors_ids''')
        rows = cur.fetchall()
        for i in rows:
            authors.append(i[1])
    except:
        authors.append('1')
    cur.close()
    base.close()
    return authors



@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    token2: str
    admin_ids: list[int]
    authors_ids: list[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    admins = get_admins()   
    authors = get_authors()   
    return Config(
        tg_bot=TgBot(
            token='',
            token2='',
            admin_ids=list(map(int, admins)),
            authors_ids=list(map(int, authors)),
            use_redis=False,
        ),
        db=DbConfig(
            host='localhost',
            password='2705GH',
            user='chat',
            database='chat',
        ),
        misc=Miscellaneous()
    )
