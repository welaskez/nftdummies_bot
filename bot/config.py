from pathlib import Path

from dotenv import load_dotenv

import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

ADMINS = os.getenv("ADMINS").split(" ")

BOT_TOKEN = os.getenv("BOT_TOKEN")
MANIFEST_URL = os.getenv("MANIFEST_URL")
MNEMONICS = os.getenv("MNEMONICS")
TONAPI_KEY = os.getenv("TONAPI_KEY")
TONCONNECT_BRIDGEAPI_KEY = os.getenv("TONCONNECT_BRIDGEAPI_KEY")

DB_URL = os.getenv("DB_URL")
DB_ECHO = True
