from aiogram import Router, types, F
from aiogram.filters import Command

from pytonconnect import TonConnect

from utils.tonconnect import connect_wallet

from keyboards.inline import inline_button, inline_keyboard

router = Router()


@router.message(Command("start"))
async def newsletter_cmd(message: types.Message):
    wallets_list = TonConnect.get_wallets()
    await message.answer("this is start command", reply_markup=inline_keyboard(
        [
            inline_button(text=wallet['name'], callback_data=f'connect_{wallet['name']}')
            for wallet in wallets_list
        ],
        adjust=2,
    ))


@router.callback_query(F.data.startswith('connect_'))
async def handle_connect_wallet(callback: types.CallbackQuery):
    wallet = callback.data.split('_')[1]
    await connect_wallet(callback, wallet)
