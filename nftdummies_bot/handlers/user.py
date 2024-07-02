from aiogram.filters import Command, CommandStart
from aiogram import Router, types

from sqlalchemy.ext.asyncio import AsyncSession

from nftdummies_bot.db.crud import create_user, get_ton_token_by_ticker
from nftdummies_bot.utils.texts import start

import hashlib

router = Router()


@router.message(CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession):
    print(f"{message.from_user.id=}")
    await create_user(session, message.from_user.id)
    await message.answer(text=start.format(message.from_user.first_name))


@router.inline_query()
async def inline_sticker(inline_query: types.InlineQuery, session: AsyncSession):
    sticker_name = inline_query.query.strip().upper()
    await inline_query.answer(
        results=[
            types.InlineQueryResultCachedSticker(
                id=hashlib.md5(sticker_name.encode()).hexdigest(),
                sticker_file_id=(
                    await get_ton_token_by_ticker(session, sticker_name)
                ).sticker_file_id,
            )
        ]
    )
