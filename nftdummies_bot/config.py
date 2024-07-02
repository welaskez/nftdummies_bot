from dotenv import load_dotenv, find_dotenv

import os

load_dotenv(find_dotenv())

BOT_TOKEN = os.getenv("BOT_TOKEN")
TONAPI_API_KEY = os.getenv("TONAPI_API_KEY")
DB_URL = os.getenv("DB_URL")
ADMINS = list(map(lambda x: int(x), os.getenv("ADMINS").split(" ")))

ECHO = True

BASE_STICKER_TEMPLATE_PATH = "nftdummies_bot/stickers/base_sticker_template.png"
BASE_FONT_PATH = "nftdummies_bot/fonts/Gagalin-Regular.ttf"
BASE_STICKERS_DIR = "nftdummies_bot/stickers"
STICKER_SET_NAME = "nftdummies_stickers_by_zireco_test_bot"
STICKER_SET_TITLE = "NFT DUMMIES STICKERS"
