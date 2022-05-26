import logging
import os
import sys
import time

import spamwatch
import telegram.ext as tg
from redis import StrictRedis
from Python_ARQ import ARQ
from pyrogram import Client, errors
from telethon.sessions import StringSession
from telethon import TelegramClient
from aiohttp import ClientSession
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

StartTime = time.time()

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("log.txt"),
        logging.StreamHandler(),
    ],
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)

LOGGER.info("[Raiden] Starting Raiden...")

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "[Raiden] You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    sys.exit(1)

ENV = bool(os.environ.get('ENV', False))

if ENV:
    TOKEN = os.environ.get('TOKEN', None)

    try:
        OWNER_ID = int(os.environ.get('OWNER_ID', None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    JOIN_LOGGER = os.environ.get('JOIN_LOGGER', None)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)

    try:
        ChICHI = set(int(x) for x in os.environ.get("DRAGONS", "").split())
        DEV_USERS = set(int(x) for x in os.environ.get("DEV_USERS", "").split())
    except ValueError:
        raise Exception(
            "Your sudo or dev users list does not contain valid integers.")

    try:
        SENPAI = set(int(x) for x in os.environ.get("DEMONS", "").split())
    except ValueError:
        raise Exception(
            "Your senpai users list does not contain valid integers.")

    try:
        SENSEI = set(int(x) for x in os.environ.get("WOLVES", "").split())
    except ValueError:
        raise Exception(
            "Your sensei users list does not contain valid integers.")

    try:
        TOMODACHI = set(int(x) for x in os.environ.get("TIGERS", "").split())
    except ValueError:
        raise Exception(
            "Your tiger users list does not contain valid integers.")

    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    URL = os.environ.get("URL", "")  # Does not contain token
    PORT = int(os.environ.get("PORT", 5000))
    CERT_PATH = os.environ.get("CERT_PATH")
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
    ARQ_API_URL = os.environ.get("ARQ_API_URL", None)
    ARQ_API_KEY = os.environ.get("ARQ_API_KEY", None)
    DB_URL = os.environ.get("DATABASE_URL") # Any SQL Database Link (RECOMMENDED:- PostgreSQL & https://www.elephantsql.com)
    REDIS_URL = os.environ.get("REDIS_URL")
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY")
    DONATION_LINK = os.environ.get("DONATION_LINK")
    LOAD = os.environ.get("LOAD", "").split()
    TEMP_DOWNLOAD_DIRECTORY = ("./")
    NO_LOAD = os.environ.get("NO_LOAD", "").split()
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", False))
 
    WORKERS = int(os.environ.get("WORKERS", 8))
    BAN_STICKER = os.environ.get("BAN_STICKER", "CAADAgADOwADPPEcAXkko5EB3YGYAg")
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", False)
    CUSTOM_CMD = os.environ.get("CUSTOM_CMD", False)
    API_WEATHER = os.environ.get("API_OPENWEATHER", None)
    WALL_API = os.environ.get("WALL_API", None)
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", None)
    API_ID = int(os.environ.get("API_ID", None))
    API_HASH = os.environ.get("API_HASH", None)
    KAZUHA_ID = os.environ.get("KAZUHA_ID", 5358835742)
    SPAMWATCH = os.environ.get("SPAMWATCH_API", None)
    SPAMMERS = os.environ.get("SPAMMERS", None)

else:
    from Raiden.config import Development as Config

    TOKEN = Config.TOKEN
    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("[Raiden] Your OWNER_ID variable is not a valid integer.")

    MESSAGE_DUMP = Config.MESSAGE_DUMP
    OWNER_USERNAME = Config.OWNER_USERNAME

    try:
        DEV_USERS = {int(x) for x in Config.DEV_USERS or []}
    except ValueError:
        raise Exception(
            "[Raiden] Your dev users list does not contain valid integers."
        )

    try:
        SUPPORT_USERS = {int(x) for x in Config.SUPPORT_USERS or []}
    except ValueError:
        raise Exception(
            "[Raiden] Your support users list does not contain valid integers."
        )

    try:
        WHITELIST_USERS = {int(x) for x in Config.WHITELIST_USERS or []}
    except ValueError:
        raise Exception(
            "[Raiden] Your whitelisted users list does not contain valid integers."
        )
    try:
        DEMONS = {int(x) for x in Config.DEMONS or []}
    except ValueError:
        raise Exception(
            "[Raiden] Your demons list does not contain valid integers."
        )
    try:
        WHITELIST_CHATS = {int(x) for x in Config.WHITELIST_CHATS or []}
    except ValueError:
        raise Exception(
            "[Raiden] Your whitelisted chats list does not contain valid integers."
        )
    try:
        BLACKLIST_CHATS = {int(x) for x in Config.BLACKLIST_CHATS or []}
    except ValueError:
        raise Exception(
            "[Raiden] Your blacklisted users list does not contain valid integers."
        )

    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH

    DB_URL = Config.DB_URL
    REDIS_URL = Config.REDIS_URL
    DONATION_LINK = Config.DONATION_LINK
    LOAD = Config.LOAD
    NO_LOAD = Config.NO_LOAD
    DEL_CMDS = Config.DEL_CMDS
    STRICT_GBAN = Config.STRICT_GBAN
    WORKERS = Config.WORKERS
    BAN_STICKER = Config.BAN_STICKER
    ALLOW_EXCL = Config.ALLOW_EXCL
    ARQ_API_URL = Config.ARQ_API_URL
    ARQ_API_KEY = Config.ARQ_API_KEY
    CUSTOM_CMD = Config.CUSTOM_CMD
    API_WEATHER = Config.API_OPENWEATHER
    WALL_API = Config.WALL_API
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    API_HASH = Config.API_HASH
    API_ID = Config.API_ID
    SPAMWATCH = Config.SPAMWATCH_API
    SPAMMERS = Config.SPAMMERS

DEV_USERS.add(OWNER_ID)
DEV_USERS.add(KAZUHA_ID)
BOT_ID = 5035068218


# Pass if SpamWatch token not set.
if SPAMWATCH is None:
    spamwtc = None
    LOGGER.warning("[Raiden] Invalid spamwatch api")
else:
    spamwtc = spamwatch.Client(SPAMWATCH)

REDIS = StrictRedis.from_url(REDIS_URL, decode_responses=True)
try:
    REDIS.ping()
    LOGGER.info("[Raiden] Your redis server is now alive!")
except BaseException:
    raise Exception("[Raiden] Your redis server is not alive, please check again.")
finally:
    REDIS.ping()
    LOGGER.info("[Raiden] Your redis server is now alive!")

session_name = TOKEN.split(":")[0]
pgram = Client(session_name, api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)

#install aiohttp session
print("Scanning AIO http session")
aiohttpsession = ClientSession() 

#install arq
print("Connecting ARQ Client")
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)
updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)
telethn = TelegramClient("Raiden", API_ID, API_HASH)
mongo_client = MongoClient(MONGO_DB_URI)
dispatcher = updater.dispatcher   

DEV_USERS = list(DEV_USERS)
WHITELIST_USERS = list(WHITELIST_USERS)
SUPPORT_USERS = list(SUPPORT_USERS)
DEMONS = list(DEMONS)

# Load at end to ensure all prev variables have been set
from Raiden.modules.helper_funcs.handlers import (CustomCommandHandler,
                                                        CustomMessageHandler,
                                                        CustomRegexHandler)

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler

print("Connecting Pyrogram Client")
pgram.start()

print("Checking Errors")

raiden = pgram.get_me()

BOT_ID = raiden.id
BOT_USERNAME = raiden.username
BOT_NAME = raiden.first_name
BOT_MENTION = raiden.mention
