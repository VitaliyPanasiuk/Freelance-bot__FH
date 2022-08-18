from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message

from tgbot.config import Config


class AuthorFilter(BaseFilter):
    is_author: bool = True

    async def __call__(self, obj: Message, config: Config) -> bool:
        return (obj.from_user.id in config.tg_bot.authors_ids) == self.is_author