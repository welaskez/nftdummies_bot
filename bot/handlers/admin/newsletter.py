from aiogram import Router, types
from aiogram.filters import Command

from filters.is_admin import IsAdmin

router = Router()
router.message.filter(IsAdmin())


@router.message(Command("newsletter"))
async def newsletter_cmd(message: types.Message):
    await message.anser("this is newsletter command")
