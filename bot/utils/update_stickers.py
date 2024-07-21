import asyncio
from db.crud.ton_token_requests import get_ton_tokens, update_sticker_fild_id

from sqlalchemy.ext.asyncio import AsyncSession

from .generate_stickers import get_stickerpack

from aiogram.exceptions import TelegramBadRequest
from aiogram import Bot

import config


async def update_stickers(bot: Bot, session: AsyncSession):
    try:
        await bot.delete_sticker_set(config.STICKER_SET_NAME)
        await bot.create_new_sticker_set(
            user_id=config.ADMINS[0],
            name=config.STICKER_SET_NAME,
            title=config.STICKER_SET_TITLE,
            stickers=await get_stickerpack(),
        )

        sticker_file_ids = [
            sticker.file_id
            for sticker in (await bot.get_sticker_set(config.STICKER_SET_NAME)).stickers
        ]

        for idx, ton_token in enumerate(await get_ton_tokens(session)):
            await update_sticker_fild_id(
                session, sticker_file_ids[idx], ton_token.ticker
            )
    except TelegramBadRequest as ex:
        print(ex)
        await asyncio.sleep(90)
        return await update_stickers(bot=bot, session=session)
