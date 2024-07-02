from PIL import Image, ImageFont, ImageDraw

from nftdummies_bot.utils.get_tokens_price.ton_tokens import get_rates
from nftdummies_bot.db.crud import get_ton_tokens
from nftdummies_bot.db.engine import session_maker
from nftdummies_bot import config

from aiogram.types import InputSticker, FSInputFile


def draw_text(
    draw: ImageDraw,
    position: tuple[int, int],
    text: str,
    font: tuple[int, int, int],
    color: tuple[int, int, int],
):
    draw.text(
        position,
        text,
        font=font,
        fill=color,
    )


def generate_sticker(
    ticker: str,
    price_ton: str,
    price_usd: str,
    diff24h: str,
    diff7d: str,
    diff30d: str,
):
    sticker = Image.open(config.BASE_STICKER_TEMPLATE_PATH)

    font_default = ImageFont.truetype(config.BASE_FONT_PATH, size=55)
    font_large = ImageFont.truetype(config.BASE_FONT_PATH, size=65)
    font_small = ImageFont.truetype(config.BASE_FONT_PATH, size=30)
    font_medium = ImageFont.truetype(config.BASE_FONT_PATH, size=32)

    draw_sticker = ImageDraw.Draw(sticker)

    draw_text(draw_sticker, (30, 120), ticker, font_default, (34, 25, 27))
    draw_text(draw_sticker, (30, 190), f"{price_ton} TON", font_small, (34, 25, 27))
    draw_text(draw_sticker, (30, 240), f"$ {price_usd}", font_large, (34, 25, 27))
    draw_text(draw_sticker, (45, 353), "7D", font_medium, (255, 255, 255))
    draw_text(draw_sticker, (297, 353), "30D", font_medium, (255, 255, 255))

    draw_text(
        draw_sticker,
        (95, 353),
        diff7d,
        font_medium,
        (0, 255, 0) if diff7d[0] == "+" else (255, 0, 0),
    )
    draw_text(
        draw_sticker,
        (358, 353),
        diff30d,
        font_medium,
        (0, 255, 0) if diff30d[0] == "+" else (255, 0, 0),
    )
    draw_text(
        draw_sticker,
        (370, 125),
        diff24h,
        font_medium,
        (0, 255, 0) if diff24h[0] == "+" else (255, 0, 0),
    )

    sticker.save(f"{config.BASE_STICKERS_DIR}/{ticker}.png")


async def get_stickerpack():
    stickers = []
    async with session_maker() as session:
        ton_tokens = await get_ton_tokens(session)
        for ton_token in ton_tokens:
            price_usd, price_ton, diff24h, diff7d, diff30d = await get_rates(
                ton_token.jetton_master_address
            )
            generate_sticker(
                ton_token.ticker, price_ton, price_usd, diff24h, diff7d, diff30d
            )
            stickers.append(
                InputSticker(
                    sticker=FSInputFile(
                        path=f"{config.BASE_STICKERS_DIR}/{ton_token.ticker}.png"
                    ),
                    format="static",
                    emoji_list=["🤑"],
                    keywords=[ton_token.ticker],
                )
            )

    return stickers
