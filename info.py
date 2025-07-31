# info.py

import os

API_ID = int(os.environ.get("API_ID", "123456"))  # Replace with your actual API ID
API_HASH = os.environ.get("API_HASH", "your_api_hash")  # Replace with your actual API HASH
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")  # Replace with your actual bot token

BOT_USERNAME = os.environ.get("BOT_USERNAME", "YourBotUsername")
PLUGINS = os.environ.get("PLUGINS", "plugins")  # Your plugins/modules folder name

# Admins and Channels
ADMINS = [int(x) for x in os.environ.get("ADMINS", "123456789").split()]
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001234567890"))  # Log channel ID
AUTH_CHANNEL = int(os.environ.get("AUTH_CHANNEL", "-1001234567890"))  # Optional: force join

# Thumbnail or Start Image
START_UP_PIC = os.environ.get("PICS", "https://telegra.ph/file/abcd12345.jpg").split()  # List of images

# Database
MONGO_URL = environ.get('MONGO_URL', "mongodb+srv://v2:v2@cluster0.9dbt2hc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# Other URLs or Settings
UPDATE_CHANNEL_URL = os.environ.get("UPDATE_CHANNEL_URL", "https://t.me/YourUpdates")
SUPPORT_GROUP_URL = os.environ.get("SUPPORT_GROUP_URL", "https://t.me/YourSupport")

# Optional Limits
FREE_USER_MAX_FILE_SIZE = int(os.environ.get("FREE_USER_MAX_FILE_SIZE", 2048))  # In MB
PREMIUM_USER_MAX_FILE_SIZE = int(os.environ.get("PREMIUM_USER_MAX_FILE_SIZE", 4096))  # In MB

# Thumbnail save path
THUMBNAIL_DIR = "./downloads/thumb/"
DOWNLOAD_DIR = "./downloads/"

# Log Channel & Developer Contact
OWNER_ID = int(os.environ.get("OWNER_ID", "123456789"))
