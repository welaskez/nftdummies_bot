from aiogram import types, Bot
from aiogram.filters import Filter

from nftdummies_bot import config


class IsAdmin(Filter):
    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        return message.from_user.id in config.ADMINS
