from aiogram import Router, types

from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.ton_token_requests import get_ton_token_by_ticker

import hashlib

router = Router()


@router.inline_query()
async def inline_sticker(inline_query: types.InlineQuery, session: AsyncSession):
    sticker_name = inline_query.query.strip().upper()
    try:
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
    except AttributeError as ex:
        print(ex)
