from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from info import START_UP_PIC, SUPPORT_GROUP, CHANNEL
from Script import script

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        buttons = [
            [InlineKeyboardButton("📢 Updates", url=CHANNEL),
             InlineKeyboardButton("❓ Help", callback_data="help_data")],
            [InlineKeyboardButton("🔎 Search", switch_inline_query_current_chat="")],
            [InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/YourUsername")]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(START_UP_PIC),
            caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )



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
