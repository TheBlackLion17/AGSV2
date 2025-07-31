import os
import re, sys
import json
import base64
import logging
import random
import asyncio
import time
import pytz
from Script import *
from datetime import datetime
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from pyrogram.types import *

from database.users_chats_db import db, delete_all_msg
from info import *
from utils import *
from database.connections_mdb import active_connection

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

TIMEZONE = "Asia/Kolkata"
BATCH_FILES = {}


@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
    btn = [
        [InlineKeyboardButton("📚 Help", callback_data="help"),
         InlineKeyboardButton("ℹ️ About", callback_data="about")],
        [InlineKeyboardButton("❌ Close", callback_data="close")]
    ]

    START_PIC = random.choice(START_PIC)
    caption = script.START_TXT.format(mention=message.from_user.mention)

    await message.reply_photo(
        photo=START_PIC,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(btn)
    )
@Client.on_callback_query()
async def cb_handler(client, query):
    if query.data == "help":
        await query.message.edit_text("🆘 Help Section Coming Soon...")
    elif query.data == "about":
        await query.message.edit_text("ℹ️ About: I'm a filter bot built with Pyrogram!")
    elif query.data == "close":
        await query.message.delete()
