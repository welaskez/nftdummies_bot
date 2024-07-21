from aiogram import Router, types
from aiogram.filters import Command

from sqlalchemy.ext.asyncio import AsyncSession

from db.crud import create_user

router = Router()


@router.message(Command("start"))
async def newsletter_cmd(message: types.Message, session: AsyncSession):
    await create_user(session=session, tg_id=message.from_user.id)
