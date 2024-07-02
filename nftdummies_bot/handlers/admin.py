from aiogram.filters import Command
from aiogram import Bot, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from sqlalchemy.ext.asyncio import AsyncSession

from nftdummies_bot.db.crud import (
    create_ton_token,
    get_ton_token_by_ticker,
    get_ton_tokens,
    update_sticker_fild_id,
    delete_ton_token
)
from nftdummies_bot.filters import IsAdmin
from nftdummies_bot.utils.get_tokens_price.ton_tokens import get_rates
from nftdummies_bot.utils.genereate_stickers import generate_sticker
from nftdummies_bot.utils import update_stickers
from nftdummies_bot import config

router = Router()
router.message.filter(IsAdmin())


class AdminStates(StatesGroup):
    sticker_data = State()
    sticker_name = State()


@router.message(Command("update_stickers"))
async def update_stickers_command(
    message: types.Message, bot: Bot, session: AsyncSession
):
    await message.answer("Updating stickers....\nIt could take a while.")
    await update_stickers(bot, session)
    await message.answer("Stickers updated!")


@router.message(Command('delete_sticker'))
async def delete_sticker_cmd(message: types.Message, state: FSMContext):
    await message.answer(
        "Write the name of the token you want to delete."
    )
    await state.set_state(AdminStates.sticker_name)


@router.message(AdminStates.sticker_name)
async def handle_delete_sticker_cmd(
    message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot
):
    await state.update_data(sticker_name=message.text.upper())
    data = await state.get_data()
    await state.clear()

    ton_token = (await get_ton_token_by_ticker(session, data['sticker_name']))
    if not ton_token:
        await message.answer("That sticker doesn't exist")
        return
    await bot.delete_sticker_from_set(
        sticker=ton_token.sticker_file_id,
    )
    await delete_ton_token(session, data['sticker_name'])

    await message.answer(f"{data['sticker_name']} succesfully deleted")
        

@router.message(Command("add_sticker"))
async def add_sticker_cmd(message: types.Message, state: FSMContext):
    await message.answer(
        "Write the name of the token and its contract address through spaces, for example a\n <i>TON EQAAAAAAAAA...</i>"
    )
    await state.set_state(AdminStates.sticker_data)


@router.message(AdminStates.sticker_data)
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
        await message.answer('Something went wrong :(\nCheck the input data and try again.')
        return
    
    if all([price_usd, price_ton, diff24h, diff7d, diff30d]):
        await create_ton_token(
            session,
            ticker=data["sticker_data"][0],
            jetton_master_address=data["sticker_data"][1],
            sticker_file_id=data["sticker_data"][0]
        )
        generate_sticker(
            data["sticker_data"][0], price_ton, price_usd, diff24h, diff7d, diff30d
        )

        await bot.add_sticker_to_set(config.ADMINS[0], config.STICKER_SET_NAME, sticker=types.InputSticker(
            sticker=types.FSInputFile(path=f"{config.BASE_STICKERS_DIR}/{data["sticker_data"][0]}.png"),
            format="static",
            keywords=[data["sticker_data"][0]],
            emoji_list=["🤑"],
        ))

        sticker_file_ids = [
            sticker.file_id
            for sticker in (await bot.get_sticker_set(config.STICKER_SET_NAME)).stickers
        ]

        await update_sticker_fild_id(session, sticker_file_ids[-1], data["sticker_data"][0])

        await message.answer(f"{data["sticker_data"][0]} succesfully added")
