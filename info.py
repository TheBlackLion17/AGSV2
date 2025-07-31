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

DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://v2:v2@cluster0.9dbt2hc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_NAME = os.environ.get("DATABASE_NAME","cluster0")
DATABASE_URI2 = environ.get('DATABASE_URI', "mongodb+srv://v2:v2@cluster0.9dbt2hc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")




CAPTION_LANGUAGES = ["Bhojpuri", "Hindi", "Bengali", "Tamil", "English", "Bangla", "Telugu", "Malayalam", "Kannada", "Marathi", "Punjabi", "Bengoli", "Gujrati", "Korean", "Gujarati", "Spanish", "French", "German", "Chinese", "Arabic", "Portuguese", "Russian", "Japanese", "Odia", "Assamese", "Urdu"]

# wes response configuration     
WEBHOOK = bool(os.environ.get("WEBHOOK", True))

# Optional Limits
FREE_USER_MAX_FILE_SIZE = int(os.environ.get("FREE_USER_MAX_FILE_SIZE", 2048))  # In MB
PREMIUM_USER_MAX_FILE_SIZE = int(os.environ.get("PREMIUM_USER_MAX_FILE_SIZE", 4096))  # In MB

# Thumbnail save path
THUMBNAIL_DIR = "./downloads/thumb/"
DOWNLOAD_DIR = "./downloads/"

MAX_B_TN = environ.get("MAX_B_TN", "5")
MAX_BTN = is_enabled((environ.get('MAX_BTN', "True")), True)


# Log Channel & Developer Contact
OWNERID = int(os.environ.get("OWNER_ID", "7705748477"))
