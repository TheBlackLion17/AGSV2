import os
import re
import time
from os import environ
from Script import *

id_pattern = re.compile(r'^.\d+$')

def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default


API_ID = int(os.environ.get("API_ID", "13357171"))  # Replace with your actual API ID
API_HASH = os.environ.get("API_HASH", "d39c4324a40a8a6b27a067f8ff2b987e")  # Replace with your actual API HASH
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8161552461:AAEIRDGMbwBDIrtjmVeD9k6DxdIf55KuN3s")  # Replace with your actual bot token
SESSION = environ.get('SESSION', 'Media_search')

BOT_USERNAME = os.environ.get("BOT_USERNAME", "agsfilterv2_bot")
PLUGINS = os.environ.get("PLUGINS", "plugins")  # Your plugins/modules folder name

# Admins and Channels
ADMINS = [int(x) for x in os.environ.get("ADMINS", "7705748477").split()]
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002801544620"))  # Log channel ID
AUTH_CHANNEL = int(os.environ.get("AUTH_CHANNEL", "-1001614481524"))  # Optional: force join
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '7705748477').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1002801544620').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
auth_grp = environ.get('AUTH_GROUP')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None


BOT_UPTIME  = time.time()
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", None)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "{file_name}")
PROTECT_CONTENT = is_enabled(environ.get('PROTECT_CONTENT', "False"), False)
START_MESSAGE = environ.get('START_MESSAGE', script.START_TXT)
FORCE_SUB_TEXT = environ.get('FORCE_SUB_TEXT', script.FORCE_SUB_TEXT)
# ============================
# Bot Settings Configuration
# ============================
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', True))

# Thumbnail or Start Image
PICS = (environ.get('PICS' ,'https://telegra.ph/file/7813a2970277d0ae265a1.jpg')).split() # List of images

# Other URLs or Settings
UPDATE_CHANNEL_URL = os.environ.get("UPDATE_CHANNEL_URL", "https://t.me/AgsModsOG")
SUPPORT_GROUP_URL = os.environ.get("SUPPORT_GROUP_URL", "https://t.me/+A9AvnxcFRNQ5Njc1")
SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "https://t.me/+A9AvnxcFRNQ5Njc1")
CHANNEL = os.environ.get("CHANNEL", "https://t.me/AgsModsOG")
MOVIE_UPDATE_CHANNEL = int(environ.get('MOVIE_UPDATE_CHANNEL', '-1002109756713'))
# Database 

DATABASE_URL = environ.get('DATABASE_URL', "mongodb+srv://v2:v2@cluster0.9dbt2hc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_NAME = os.environ.get("DATABASE_NAME","cluster0")
DATABASE_URL2 = environ.get('DATABASE_URL2', "mongodb+srv://v2:v2@cluster0.9dbt2hc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
FILE_DB_URL = environ.get("FILE_DB_URL", DATABASE_URL)
FILE_DB_NAME = environ.get("FILE_DB_NAME", DATABASE_NAME)
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')


WELCOM_PIC = environ.get("WELCOM_PIC", "https://graph.org/file/01ddfcb1e8203879a63d7.jpg")
WELCOM_TEXT = environ.get("WELCOM_TEXT", script.WELCOM_TEXT)
PMFILTER = is_enabled(environ.get('PMFILTER', "True"), True)
G_FILTER = is_enabled(environ.get("G_FILTER", "True"), True)
BUTTON_LOCK = is_enabled(environ.get("BUTTON_LOCK", "True"), True)
RemoveBG_API = environ.get("RemoveBG_API", "")
BUTTON_LOCK_TEXT = environ.get("BUTTON_LOCK_TEXT", script.BUTTON_LOCK_TEXT)
# url shortner
SHORT_URL = environ.get("SHORT_URL")
SHORT_API = environ.get("SHORT_API")



CAPTION_LANGUAGES = ["Bhojpuri", "Hindi", "Bengali", "Tamil", "English", "Bangla", "Telugu", "Malayalam", "Kannada", "Marathi", "Punjabi", "Bengoli", "Gujrati", "Korean", "Gujarati", "Spanish", "French", "German", "Chinese", "Arabic", "Portuguese", "Russian", "Japanese", "Odia", "Assamese", "Urdu"]

# wes response configuration     
WEBHOOK = bool(os.environ.get("WEBHOOK", True))

# Optional Limits
FREE_USER_MAX_FILE_SIZE = int(os.environ.get("FREE_USER_MAX_FILE_SIZE", 2048))  # In MB
PREMIUM_USER_MAX_FILE_SIZE = int(os.environ.get("PREMIUM_USER_MAX_FILE_SIZE", 4096))  # In MB

# Thumbnail save path
THUMBNAIL_DIR = "./downloads/thumb/"
DOWNLOAD_DIR = "./downloads/"

MAX_RIST_BTNS = int(environ.get('MAX_RIST_BTNS', "10"))
MAX_RIST_BTNS = is_enabled((environ.get('MAX_RIST_BTNS', "True")), True)


# Log Channel & Developer Contact
OWNERID = int(os.environ.get("OWNER_ID", "7705748477"))
SINGLE_BUTTON = is_enabled(environ.get('SINGLE_BUTTON', "True"), True)
P_TTI_SHOW_OFF = is_enabled(environ.get('P_TTI_SHOW_OFF', "True"), True)
IMDB_DELET_TIME = int(environ.get('IMDB_DELET_TIME', "300"))
IMDB = is_enabled(environ.get('IMDB', "False"), True)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", script.IMDB_TEMPLATE)
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split()]
MELCOW_NEW_USERS = is_enabled(environ.get('MELCOW_NEW_USERS', "True"), True)
PROTECT_CONTENT = is_enabled(environ.get('PROTECT_CONTENT', "False"), False)
PUBLIC_FILE_STORE = is_enabled(environ.get('PUBLIC_FILE_STORE', "True"), True)
PM_IMDB = is_enabled(environ.get('PM_IMDB', "False"), True)
