import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

from tgbot.config import load_config
from tgbot.handlers_user.admin import admin_router
from tgbot.handlers_user.user import user_router
from tgbot.handlers_author.author import author_router
from tgbot.misc.function import author2_router, alert8,alert12,alert16,start_search,genid_crm,check_coeff,change_coeff_author
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.services import broadcaster
from tgbot.db import start_db

logger = logging.getLogger(__name__)


# async def on_startup(bot: Bot, admin_ids: list[int]):
#     await broadcaster.broadcast(bot, admin_ids, "Бот був запущений")


def register_global_middlewares(dp: Dispatcher, config):
    dp.message.outer_middleware(ConfigMiddleware(config))
    dp.callback_query.outer_middleware(ConfigMiddleware(config))


async def main():
    await start_db.postgre_start()
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    bot2 = Bot(token=config.tg_bot.token2, parse_mode='HTML')
    dp = Dispatcher(storage=storage)
    dp2 = Dispatcher(storage=storage)

    for router in [
        user_router,
    ]:
        dp.include_router(router)
    for router in [
        admin_router,
        author_router,
        author2_router,  
    ]:
        dp2.include_router(router)

    register_global_middlewares(dp, config)
    register_global_middlewares(dp2, config)

    # await on_startup(bot, config.tg_bot.admin_ids)
    # await on_startup(bot2, config.tg_bot.admin_ids)
    # , alert8(), alert12(), alert16()
    await asyncio.gather(dp.start_polling(bot), dp2.start_polling(bot2), start_search(),genid_crm(),check_coeff(),change_coeff_author())


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Бот був вимкнений!")
