from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def newsletter_cmd(message: types.Message):
    await message.answer("this is start command")
