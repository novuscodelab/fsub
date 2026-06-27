import os

from dotenv import load_dotenv
from logging import basicConfig, INFO, WARNING, getLogger, Logger

load_dotenv("config.env", override=True)


def parse_int(value, default=0):
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def parse_bool(value, default=False):
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def parse_int_list(value):
    ids = []
    for item in str(value or "").replace(",", " ").split():
        parsed = parse_int(item, None)
        if parsed is not None:
            ids.append(parsed)
    return ids


BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_DB = parse_int(os.getenv("CHANNEL_DB"))
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fsub_bot")

RESTRICT = parse_bool(os.getenv("RESTRICT"), True)

BUTTON_TITLE = os.getenv("BUTTON_TITLE", "ᴊᴏɪɴ")
BUTTON_ROW = max(1, parse_int(os.getenv("BUTTON_ROW", 2), 2))

FORCE_SUB_ = {}
FSUB_TOTAL = 1
while True:
    key = f"FORCE_SUB_{FSUB_TOTAL}"
    value = os.getenv(key)
    if value is None:
        break
    chat_id = parse_int(value, None)
    if chat_id is not None:
        FORCE_SUB_[FSUB_TOTAL] = chat_id
    FSUB_TOTAL += 1

START_MESSAGE = os.getenv(
    "START_MESSAGE",
    "Halo {mention}!"
    "\n\n"
    "Saya dapat menyimpan file pribadi di Channel tertentu dan pengguna lain dapat mengaksesnya dari link khusus.",
)
FORCE_MESSAGE = os.getenv(
    "FORCE_MESSAGE",
    "Halo {mention}!"
    "\n\n"
    "Hayolo Ketahuan Belum Join Channel dan Groupnya Yaa, Yuk Join Dulu Biar Bisa Buka Linknya."
    "\n\n"
    "Silakan Join Ke Channel dan Groupnya di Bawah Ini Terlebih Dahulu Yaa.",
    )
SUPER_USERS = [6608388199, 7494727691]
ADMINS = list(dict.fromkeys(parse_int_list(os.getenv("ADMINS", "")) + SUPER_USERS))
OWNERS = list(
    dict.fromkeys(parse_int_list(os.getenv("OWNER", os.getenv("OWNERS", ""))) + SUPER_USERS)
)
    
CUSTOM_CAPTION = os.getenv("CUSTOM_CAPTION", None)
DISABLE_BUTTON = parse_bool(os.getenv("DISABLE_BUTTON"), False)


basicConfig(level=INFO, format="[%(levelname)s] - %(message)s")
getLogger("hydrogram").setLevel(WARNING)
def LOGGER(name: str) -> Logger:
    return getLogger(name)
