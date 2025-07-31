import os
from os import environ


API_ID = int(os.environ.get("API_ID", "13357171"))  # Replace with your actual API ID
API_HASH = os.environ.get("API_HASH", "d39c4324a40a8a6b27a067f8ff2b987e")  # Replace with your actual API HASH
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8161552461:AAEIRDGMbwBDIrtjmVeD9k6DxdIf55KuN3s")  # Replace with your actual bot token

BOT_USERNAME = os.environ.get("BOT_USERNAME", "agsfilterv2_bot")
PLUGINS = os.environ.get("PLUGINS", "plugins")  # Your plugins/modules folder name

# Admins and Channels
ADMINS = [int(x) for x in os.environ.get("ADMINS", "7705748477").split()]
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002801544620"))  # Log channel ID
AUTH_CHANNEL = int(os.environ.get("AUTH_CHANNEL", "-1001614481524"))  # Optional: force join

BOT_UPTIME  = time.time()

# Thumbnail or Start Image
START_UP_PIC = (environ.get('START_UP_PICS' ,'https://telegra.ph/file/7813a2970277d0ae265a1.jpg')).split() # List of images

# Other URLs or Settings
UPDATE_CHANNEL_URL = os.environ.get("UPDATE_CHANNEL_URL", "https://t.me/AgsModsOG")
SUPPORT_GROUP_URL = os.environ.get("SUPPORT_GROUP_URL", "https://t.me/+A9AvnxcFRNQ5Njc1")
SUPPORT_GROUP = os.environ.get("SUPPORT_GROUP", "https://t.me/+A9AvnxcFRNQ5Njc1")
CHANNEL = os.environ.get("CHANNEL", "https://t.me/AgsModsOG")

# Database 

MONGO_URL = environ.get('MONGO_URL', "mongodb+srv://v2:v2@cluster0.9dbt2hc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")


# wes response configuration     
WEBHOOK = bool(os.environ.get("WEBHOOK", True))

# Optional Limits
FREE_USER_MAX_FILE_SIZE = int(os.environ.get("FREE_USER_MAX_FILE_SIZE", 2048))  # In MB
PREMIUM_USER_MAX_FILE_SIZE = int(os.environ.get("PREMIUM_USER_MAX_FILE_SIZE", 4096))  # In MB

# Thumbnail save path
THUMBNAIL_DIR = "./downloads/thumb/"
DOWNLOAD_DIR = "./downloads/"

# Log Channel & Developer Contact
OWNER_ID = int(os.environ.get("OWNER_ID", "7705748477"))
