from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db.models import User


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
