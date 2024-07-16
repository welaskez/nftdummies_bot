from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


def inline_keyboard(
    buttons: list[InlineKeyboardButton],
    adjust: int = 1,
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    for button in buttons:
        keyboard.add(button)

    return keyboard.adjust(
        adjust,
    ).as_markup()


def inline_button(
    text: str,
    callback_data: str = None,
    url: str = None,
    webapp: WebAppInfo = None,
) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=text,
        callback_data=callback_data,
        url=url,
        web_app=webapp,
    )
