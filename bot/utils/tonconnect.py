from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    BufferedInputFile,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from pytonconnect import TonConnect
from pytonconnect.storage import FileStorage
from pytonconnect.parsers import WalletInfo

from pytoniq_core import Address

from nacl.utils import random

from datetime import datetime

from io import BytesIO

from typing import Any

import asyncio
import qrcode
import config


def get_storage(chat_id: int) -> FileStorage:
    return FileStorage(file_path=f"{config.BASE_DIR}/connections/{chat_id}.json")


def generate_payload(ttl: int) -> str:
    payload = bytearray(random(8))

    ts = int(datetime.now().timestamp()) + ttl
    payload.extend(ts.to_bytes(8, "big"))

    return payload.hex()


def check_payload(payload: str, wallet_info: WalletInfo) -> bool:
    if len(payload) < 32:
        print("Payload length error!")
        return False
    if not wallet_info.check_proof(payload):
        print("Check proof failed!")
        return False
    ts = int(payload[16:32], 16)
    if datetime.now().timestamp() > ts:
        print("Request timeout error!")
        return False

    return True


def generate_qr(url: str) -> BufferedInputFile:
    img = qrcode.make(url)
    stream = BytesIO()
    img.save(stream)
    file = BufferedInputFile(file=stream.getvalue(), filename="qrcode")

    return file


def get_connector(chat_id: int) -> TonConnect:
    return TonConnect(
        config.MANIFEST_URL,
        storage=get_storage(chat_id),
        api_tokens={"tonapi": "7ca1f081609976ddb8d4935c3c5c8654"},
    )


async def disconnect_wallet(tg_id: int) -> None:
    connector = get_connector(tg_id)
    await connector.restore_connection()
    await connector.disconnect()


async def connect_wallet(callback: CallbackQuery, wallet_name: str) -> bool | Any:
    proof_payload = generate_payload(600)

    connector = get_connector(callback.from_user.id)

    proof = True

    def status_changed(wallet_info):
        nonlocal proof
        if wallet_info is not None:
            proof = check_payload(proof_payload, wallet_info)

        unsubscribe()

    def status_error(e):
        print("Connect error: ", e)

    unsubscribe = connector.on_status_change(status_changed, status_error)

    wallet = None

    for w in connector.get_wallets():
        if w["name"] == wallet_name:
            wallet = w

    if wallet is None:
        raise Exception(f"Unknown wallet: {wallet_name}")

    generated_url = await connector.connect(
        wallet,
        {"ton_proof": proof_payload},
    )

    mk_b = InlineKeyboardBuilder()
    mk_b.button(text="Connect", url=generated_url)

    qr = generate_qr(generated_url)

    photo_message = await callback.message.answer_photo(
        photo=qr,
        caption="Жми connect и подключи свой кошелек.\nСcылка действительна в течении трех минут.",
        reply_markup=mk_b.as_markup(),
    )

    for _ in range(180):
        await asyncio.sleep(1)
        if connector.connected:
            if not proof:
                await disconnect_wallet(callback.from_user.id)
                await photo_message.delete()
                await callback.message.answer(
                    "Подумай еще 3 раза.",
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text="На главную", callback_data="main"
                                )
                            ]
                        ]
                    ),
                )
                return
            if connector.account.address:
                await disconnect_wallet(callback.from_user.id)
                wallet_address = Address(connector.account.address).to_str(
                    is_bounceable=False
                )
                await photo_message.delete()
                return wallet_address

    await callback.message.answer(
        text="К сожаления, время вышло.\nПерейди на главную и попробуй снова.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="На главную", callback_data="main")]
            ]
        ),
    )

    return False
