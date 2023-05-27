import re
from os import environ
import asyncio
import json
from collections import defaultdict
from typing import Dict, List, Union
from pyrogram import Client
from time import time

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.strip().lower() in ["on", "true", "yes", "1", "enable", "y"]:
        return True
    elif value.strip().lower() in ["off", "false", "no", "0", "disable", "n"]:
        return False
    else:
        return default


# Bot information
PORT = environ.get("PORT", "8080")
WEBHOOK = bool(environ.get("WEBHOOK", True)) # for web support on/off
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', True))
PICS = (environ.get('PICS' ,'https://graph.org/file/01ddfcb1e8203879a63d7.jpg https://graph.org/file/d69995d9846fd4ad632b8.jpg https://graph.org/file/a125497b6b85a1d774394.jpg https://graph.org/file/43d26c54d37f4afb830f7.jpg https://graph.org/file/60c1adffc7cc2015f771c.jpg https://graph.org/file/d7b520240b00b7f083a24.jpg https://graph.org/file/0f336b0402db3f2a20037.jpg https://graph.org/file/39cc4e15cad4519d8e932.jpg https://graph.org/file/d59a1108b1ed1c6c6c144.jpg https://te.legra.ph/file/3a4a79f8d5955e64cbb8e.jpg https://graph.org/file/d69995d9846fd4ad632b8.jpg')).split()
BOT_START_TIME = time()

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '0').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
auth_grp = environ.get('AUTH_GROUP')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "")
DATABASE_NAME = environ.get('DATABASE_NAME', "Cluster0")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

#maximum search result buttos count in number#
MAX_RIST_BTNS = int(environ.get('MAX_RIST_BTNS', "10"))
START_MESSAGE = environ.get('START_MESSAGE', '👋 𝙷𝚎𝚕𝚕𝚘 {user}\n\n𝙼𝚢𝚜𝚎𝚕𝚏 {bot},\n\n𝚃𝚛𝚞𝚜𝚝 𝚖𝚎 !  𝙸 𝚌𝚊𝚗𝚗𝚘𝚝 𝚎𝚟𝚎𝚗 𝚒𝚖𝚊𝚐𝚒𝚗𝚎 𝚑𝚘𝚠 𝚜𝚞𝚙𝚎𝚛-𝚏𝚊𝚜𝚝 𝙸 𝚌𝚊𝚗 𝚍𝚛𝚒𝚟𝚎 𝚢𝚘𝚞𝚛 𝙳𝚊𝚝𝚊𝚋𝚊𝚜𝚎 𝚌𝚑𝚊𝚗𝚗𝚎𝚕. \n\n𝙰𝚛𝚎 𝚢𝚘𝚞 𝚛𝚎𝚊𝚍𝚢 𝚏𝚘𝚛 𝙻𝚘𝚗𝚐 𝙳𝚛𝚒𝚟𝚎 𝙱𝚊𝚋𝚢...🤪')
BUTTON_LOCK_TEXT = environ.get("BUTTON_LOCK_TEXT", "⚠️ 𝙷𝚎𝚢 {query}! 𝚃𝚑𝚊𝚝'𝚜 𝚗𝚘𝚝 𝚏𝚘𝚛 𝚢𝚘𝚞. 𝙿𝚕𝚎𝚊𝚜𝚎 𝚛𝚎𝚚𝚞𝚎𝚜𝚝 𝚢𝚘𝚞𝚛 𝚘𝚠𝚗.")
FORCE_SUB_TEXT = environ.get('FORCE_SUB_TEXT', '𝙿𝚕𝚎𝚊𝚜𝚎 𝚓𝚘𝚒𝚗 𝚖𝚢 𝚞𝚙𝚍𝚊𝚝𝚎𝚜 𝚌𝚑𝚊𝚗𝚗𝚎𝚕 𝚒𝚗 𝚘𝚛𝚍𝚎𝚛 𝚝𝚘 𝚞𝚜𝚎 𝚖𝚎.')
RemoveBG_API = environ.get("RemoveBG_API", "")
WELCOM_PIC = environ.get("WELCOM_PIC", "")
WELCOM_TEXT = environ.get("WELCOM_TEXT", "𝙷𝚎𝚢 {user}\n\n 𝚆𝚎𝚕𝚌𝚘𝚖𝚎 𝚝𝚘 𝚝𝚑𝚎 @FilmsofFortune 𝙼𝚘𝚟𝚒𝚎 𝚁𝚎𝚚𝚞𝚎𝚜𝚝 𝙶𝚛𝚘𝚞𝚙!")
PMFILTER = environ.get('PMFILTER', "True")
G_FILTER = bool(environ.get("G_FILTER", True))
BUTTON_LOCK = environ.get("BUTTON_LOCK", "True")

# url shortner
SHORT_URL = environ.get("SHORT_URL")
SHORT_API = environ.get("SHORT_API")

# Others
IMDB_DELET_TIME = int(environ.get('IMDB_DELET_TIME', "300"))
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', 0))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'FilmsofFortune')
P_TTI_SHOW_OFF = is_enabled((environ.get('P_TTI_SHOW_OFF', "True")), True)
PM_IMDB = environ.get('PM_IMDB', "True")
IMDB = is_enabled((environ.get('IMDB', "True")), True)
SINGLE_BUTTON = is_enabled((environ.get('SINGLE_BUTTON', "True")), True)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "🎭 <b>𝐅𝐢𝐥𝐞 𝐔𝐩𝐥𝐨𝐚𝐝𝐞𝐝 𝐁𝐲 :\n   ❣[𝙵𝙸𝙻𝙼𝚂 𝙾𝙵 𝙵𝙾𝚁𝚃𝚄𝙽𝙴](https://t.me/FilmsofFortune)</b>❣\n\n🎬 <b>File Name: </b> ➥  <i>{file_name}</i>\n⚙️ <b>Size: </b><i>{file_size}</i>\n\n   <b>👇New Updates Join Now👇</b>\n\n⚡  ↭ <b>[𝙵𝙸𝙻𝙼𝚂 𝙾𝙵 𝙵𝙾𝚁𝚃𝚄𝙽𝙴](https://t.me/FilmsofFortune)</b> ↭  ⚡")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "<b>Query: {query}</b> \n‌IMDb Data:\n\n👻 Title: <a href={url}>{title}</a>\n🎭 Genres: {genres}\n🥳 Year: <a href={url}/releaseinfo>{year}</a>\n❣ Rating: <a href={url}/ratings>{rating}</a> / 10")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split()]
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "True")), True)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "True")), True)
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "True")), True)

#request force sub
REQ_SUB = bool(environ.get("REQ_SUB", True))
SESSION_STRING = environ.get("SESSION_STRING", "")









