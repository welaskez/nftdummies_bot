from aiogram.filters import Command
from aiogram import Router, types

from utils.messages import admin

from filters.is_admin import IsAdmin

router = Router()
router.message.filter(IsAdmin())


@router.message(Command("admin"))
async def admin_cmd(message: types.Message):
    await message.answer(text=admin)
