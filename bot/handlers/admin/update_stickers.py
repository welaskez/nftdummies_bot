from aiogram import Router, Bot, types
from aiogram.filters import Command

from filters.is_admin import IsAdmin

from sqlalchemy.ext.asyncio import AsyncSession

from utils import update_stickers

router = Router()
router.message.filter(IsAdmin())


@router.message(Command("update_stickers"))
async def newsletter_cmd(message: types.Message, bot: Bot, session: AsyncSession):
    await message.answer("Updating stickers....\nIt could take a while.")
    await update_stickers(bot, session)
    await message.answer("Stickers updated!")
