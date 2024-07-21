from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.fsm.context import FSMContext
from aiogram import Router, Bot, types
from aiogram.filters import Command

from db.crud.ton_token_requests import get_ton_token_by_ticker, delete_ton_token

from states import AdminState

router = Router()


@router.message(Command("delete_sticker"))
async def delete_sticker_cmd(message: types.Message, state: FSMContext):
    await message.answer("Write the name of the token you want to delete.")
    await state.set_state(AdminState.sticker_name)


@router.message(AdminState.sticker_name)
async def handle_delete_sticker_cmd(
    message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot
):
    await state.update_data(sticker_name=message.text.upper())
    data = await state.get_data()
    await state.clear()

    ton_token = await get_ton_token_by_ticker(session, data["sticker_name"])
    if not ton_token:
        await message.answer("That sticker doesn't exist")
        return
    await bot.delete_sticker_from_set(
        sticker=ton_token.sticker_file_id,
    )
    await delete_ton_token(session, data["sticker_name"])

    await message.answer(f"{data['sticker_name']} succesfully deleted")
