from dataclasses import dataclass

from environs import Env

DB_URI = 'postgres://dciydempsuflmu:c58efd2b3ec4d432bcdccf401c5343ca2c09c3c6d8d9f1e8f2698330e3572ff3@ec2-50-19-255-190.compute-1.amazonaws.com:5432/db03aoprqprn98'
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
            token=env.str("BOT_TOKEN"),
            token2=env.str("BOT_TOKEN2"),
            admin_ids=list(map(int, admins)),
            authors_ids=list(map(int, authors)),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        misc=Miscellaneous()
    )
