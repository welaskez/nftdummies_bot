from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.fsm.context import FSMContext
from aiogram import Router, Bot, types
from aiogram.filters import Command

from db.crud.ton_token_requests import create_ton_token, update_sticker_fild_id

from states import AdminState

from filters.is_admin import IsAdmin

from utils.generate_stickers import generate_sticker
from utils.get_tokens_price.ton_tokens import get_rates

import config

router = Router()
router.message.filter(IsAdmin())


@router.message(Command("add_sticker"))
async def add_sticker_cmd(message: types.Message, state: FSMContext):
    await message.answer(
        "Write the name of the token and its contract address through spaces, for example a\n <i>TON EQAAAAAAAAA...</i>"
    )
    await state.set_state(AdminState.sticker_data)


@router.message(AdminState.sticker_data)
async def handle_add_sticker_cmd(
    message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot
):
    sticker_data = message.text.split()

    if len(sticker_data) != 2:
        await message.answer("Wrong format\nTry again or take another look.")
        return

    await state.update_data(sticker_data=sticker_data)
    data = await state.get_data()
    await state.clear()

    try:
        price_usd, price_ton, diff24h, diff7d, diff30d = await get_rates(
            data["sticker_data"][1]
        )
    except Exception as e:
        print(f"Error when adding a sticker: {e}")
        await message.answer(
            "Something went wrong :(\nCheck the input data and try again."
        )
        return

    if all([price_usd, price_ton, diff24h, diff7d, diff30d]):
        await create_ton_token(
            session,
            ticker=data["sticker_data"][0],
            jetton_master_address=data["sticker_data"][1],
            sticker_file_id=data["sticker_data"][0],
        )
        generate_sticker(
            data["sticker_data"][0], price_ton, price_usd, diff24h, diff7d, diff30d
        )

        await bot.add_sticker_to_set(
            config.ADMINS[0],
            config.STICKER_SET_NAME,
            sticker=types.InputSticker(
                sticker=types.FSInputFile(
                    path=f"{config.BASE_STICKERS_DIR}/{data['sticker_data'][0]}.png"
                ),
                format="static",
                keywords=[data["sticker_data"][0]],
                emoji_list=["🤑"],
            ),
        )

        sticker_file_ids = [
            sticker.file_id
            for sticker in (await bot.get_sticker_set(config.STICKER_SET_NAME)).stickers
        ]

        await update_sticker_fild_id(
            session, sticker_file_ids[-1], data["sticker_data"][0]
        )

        await message.answer(f"{data['sticker_data'][0]} succesfully added")
