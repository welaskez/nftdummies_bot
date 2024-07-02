from aiogram import Bot

from nftdummies_bot import config
from nftdummies_bot.db.crud import get_ton_tokens, update_sticker_fild_id

from sqlalchemy.ext.asyncio import AsyncSession

from .genereate_stickers import get_stickerpack


async def update_stickers(bot: Bot, session: AsyncSession):
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
        await update_sticker_fild_id(session, sticker_file_ids[idx], ton_token.ticker)
