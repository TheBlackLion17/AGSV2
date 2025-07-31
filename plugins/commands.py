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


@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if EMOJI_MODE:    
        await message.react(emoji=random.choice(REACTIONS), big=True) 
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        buttons = [[
                    InlineKeyboardButton('• ᴀᴅᴅ ᴍᴇ ᴛᴏ ᴜʀ ᴄʜᴀᴛ •', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
                ],[
                    InlineKeyboardButton('• ᴍᴀsᴛᴇʀ •', url="https://t.me/cosmic_freak"),
                    InlineKeyboardButton('• sᴜᴘᴘᴏʀᴛ •', url='https://t.me/codeflixsupport')
                ],[
                    InlineKeyboardButton('• ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ •', url="https://t.me/codeflix_bots")
                  ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply(script.GSTART_TXT.format(message.from_user.mention if message.from_user else message.chat.title, temp.U_NAME, temp.B_NAME), reply_markup=reply_markup, disable_web_page_preview=True)
        await asyncio.sleep(2) 
        if not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "Unknown"))       
            await db.add_chat(message.chat.id, message.chat.title)
        return 
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
