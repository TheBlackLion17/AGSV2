import random
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import CHANNEL, START_UP_PIC
from Script import script
from database.users_chats_db import userdb  # Import the correct object

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        buttons = [
            [
                InlineKeyboardButton("📢 Updates", url=CHANNEL),
                InlineKeyboardButton("❓ Help", callback_data="help_data")
            ],
            [
                InlineKeyboardButton("🔎 Search", switch_inline_query_current_chat=""),
                InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/YourUsername")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(START_UP_PIC),
            caption=script.START_TXT.format(
                message.from_user.mention,
                client.me.first_name,
                client.me.username
            ),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    else:
        # Add user to DB if not exists
        if not await userdb.is_user(message.from_user.id):
            await userdb.add_user(message.from_user.id, message.from_user.first_name)

        buttons = [
            [
                InlineKeyboardButton("📢 Updates", url=CHANNEL),
                InlineKeyboardButton("❓ Help", callback_data="help_data")
            ],
            [
                InlineKeyboardButton("🔎 Search", switch_inline_query_current_chat=""),
                InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/YourUsername")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(START_UP_PIC),
            caption=script.START_TXT.format(
                message.from_user.mention,
                client.me.first_name,
                client.me.username
            ),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
