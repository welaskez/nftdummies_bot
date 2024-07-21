from pathlib import Path

from dotenv import load_dotenv

import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

ADMINS = list(map(lambda admin_id: int(admin_id), os.getenv("ADMINS").split(" ")))

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_NAME = os.getenv("BOT_NAME")
TONAPI_KEY = os.getenv("TONAPI_KEY")

DB_URL = os.getenv("DB_URL")
DB_ECHO = True

BASE_STICKER_TEMPLATE_PATH = f"{BASE_DIR}/stickers/base_sticker_template.png"
BASE_FONT_PATH = f"{BASE_DIR}/fonts/Gagalin-Regular.ttf"
BASE_STICKERS_DIR = f"{BASE_DIR}/stickers"
STICKER_SET_NAME = f"nftdummies_stickers_by_{BOT_NAME}"
STICKER_SET_TITLE = "NFT DUMMIES STICKERS"
