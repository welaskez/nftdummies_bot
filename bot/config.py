from dotenv import load_dotenv

import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MANIFEST_URL = os.getenv("MANIFEST_URL")
DB_URL = os.getenv("DB_URL")
DB_ECHO = True
MNEMONICS = os.getenv("MNEMONICS")
TONAPI_KEY = os.getenv("TONAPI_KEY")
