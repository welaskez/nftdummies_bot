from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import ScalarResult, select

from nftdummies_bot.db.models import TonToken, User


async def create_ton_token(
    session: AsyncSession,
    ticker: str,
    jetton_master_address: str,
    sticker_file_id: str,
) -> TonToken:
    ton_token = TonToken(
        ticker=ticker,
        jetton_master_address=jetton_master_address,
        sticker_file_id=sticker_file_id,
    )

    session.add(ton_token)
    await session.commit()
    await session.refresh(ton_token)
    return ton_token


async def get_ton_token_by_ticker(
    session: AsyncSession,
    ticker: str,
) -> TonToken | None:
    ton_token = await session.scalar(select(TonToken).where(TonToken.ticker == ticker))
    return ton_token


async def update_sticker_fild_id(
    session: AsyncSession,
    sticker_file_id: str,
    ticker: str,
) -> None:
    ton_token = await get_ton_token_by_ticker(session, ticker)
    if ton_token:
        ton_token.sticker_file_id = sticker_file_id
        await session.commit()
        await session.refresh(ton_token)


async def delete_ton_token(
    session: AsyncSession,
    ticker: str,
):
    ton_token = await get_ton_token_by_ticker(session, ticker)
    if ton_token:
        await session.delete(ton_token)
        await session.commit()


async def get_ton_tokens(session: AsyncSession) -> ScalarResult[TonToken]:
    ton_tokens: ScalarResult[TonToken] = await session.scalars(select(TonToken))
    return ton_tokens


async def create_user(session: AsyncSession, tg_id: int) -> User:
    user = await get_user_by_tg_id(session, tg_id)
    if not user:
        user = User(tg_id=tg_id)
        session.add(user)
        await session.commit()
        await session.refresh(user)


async def get_user_by_tg_id(session: AsyncSession, tg_id: int) -> User | None:
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    return user
