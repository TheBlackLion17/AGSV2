from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import enums
from database.users_chats_db import db

from pyrogram.enums import ChatType
from info import START_UP_PIC, SUPPORT_GROUP, CHANNEL
from Script import script

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    user_mention = message.from_user.mention if message.from_user else message.chat.title

    # Group / Supergroup handling
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        buttons = [
            [InlineKeyboardButton('⛩️ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ ⛩️', url=f'https://t.me/{SUPPORT_CHAT}')],
            [InlineKeyboardButton('💁‍♂️ sᴇᴇ ᴍᴇ 💁‍♂️', url=f"https://t.me/{temp.U_NAME}?start=help")]
        ]
        await message.reply(
            START_MESSAGE.format(user=user_mention, bot=client.mention),
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )
        await asyncio.sleep(2)

        # Add group to database if not exists
        if not await db.get_chat(message.chat.id):
            total_members = await client.get_chat_members_count(message.chat.id)
            await client.send_message(
                LOG_CHANNEL,
                script.LOG_TEXT_G.format(
                    a=message.chat.title,
                    b=message.chat.id,
                    c=message.chat.username,
                    d=total_members,
                    f=client.mention,
                    e="Unknown"
                )
            )
            await db.add_chat(message.chat.id, message.chat.title, message.chat.username)
        return

    # Private chat logic
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(
            LOG_CHANNEL,
            script.LOG_TEXT_P.format(
                message.from_user.id,
                user_mention,
                message.from_user.username,
                temp.U_NAME
            )
        )

    # If /start is just plain or invalid args
    if len(message.command) != 2:
        buttons = [
            [InlineKeyboardButton("⇋ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ⇋", url=f"http://t.me/{temp.U_NAME}?startgroup=true")],
            [
                InlineKeyboardButton("📢 𝗢𝘁𝘁 𝗨𝗽𝗱𝗮𝘁𝗲𝘃 📢", url="https://t.me/+RDsxY-lQ55wwOWI1"),
                InlineKeyboardButton("🚧 𝗕𝗼𝘁 𝗨𝗽𝗱𝗮𝘁𝗲 🚧", url="https://t.me/AgsModsOG")
            ],
            [InlineKeyboardButton("⚡𝗠𝗼𝘃𝗲 𝗖𝗵𝗮𝗻𝗻𝗲𝗹⚡", url="https://t.me/Movies_Hub_OG")]
        ]

        m = await message.reply_sticker("CAACAgUAAxkBAAJZtmZSPxpeDEIwobQtSQnkeGbwNjsyAAJjDgACjPuwVS9WyYuOlsqENQQ")
        await asyncio.sleep(2)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=START_MESSAGE.format(user=user_mention, bot=client.mention),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )
        return await m.delete()



@Client.on_message(filters.command("help") & filters.private)
async def help_cmd(client, message: Message):
    await message.reply_photo(
        photo=START_UP_PIC,
        caption=script.HELP_TXT,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Home", callback_data="start_data"),
             InlineKeyboardButton("📢 Channel", url=CHANNEL)],
            [InlineKeyboardButton("💬 Support", url=SUPPORT_GROUP)]
        ])
    )


@Client.on_message(filters.command("about") & filters.private)
async def about_cmd(client, message: Message):
    await message.reply_photo(
        photo=START_UP_PIC,
        caption=script.ABOUT_TXT,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="help_data"),
             InlineKeyboardButton("🏠 Home", callback_data="start_data")]
        ])
    )


@Client.on_callback_query()
async def cb_data(client, callback_query):
    data = callback_query.data

    if data == "start_data":
        await callback_query.message.edit_media(
            media=START_UP_PIC,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Updates", url=CHANNEL),
                 InlineKeyboardButton("❓ Help", callback_data="help_data")],
                [InlineKeyboardButton("🔎 Search", switch_inline_query_current_chat="")]
            ])
        )
        await callback_query.message.edit_caption(
            caption=script.START_TXT.format(callback_query.from_user.mention)
        )

    elif data == "help_data":
        await callback_query.message.edit_caption(
            caption=script.HELP_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Home", callback_data="start_data"),
                 InlineKeyboardButton("📢 Channel", url=CHANNEL)],
                [InlineKeyboardButton("💬 Support", url=SUPPORT_GROUP)]
            ])
        )

    elif data == "about_data":
        await callback_query.message.edit_caption(
            caption=script.ABOUT_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="help_data"),
                 InlineKeyboardButton("🏠 Home", callback_data="start_data")]
            ])
        )
