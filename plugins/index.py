import logging
import asyncio
import re
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import (
    ChannelInvalid,
    ChatAdminRequired,
    UsernameInvalid,
    UsernameNotModified,
)
from info import ADMINS, INDEX_REQ_CHANNEL as LOG_CHANNEL
from database.ia_filterdb import save_file, MediaWrapper
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import temp

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lock = asyncio.Lock()


@Client.on_callback_query(filters.regex(r'^index'))
async def index_files(bot, query):
    if query.data.startswith('index_cancel'):
        temp.CANCEL = True
        return await query.answer("Cancelling Indexing")

    _, action, chat, lst_msg_id, from_user = query.data.split("#")

    if action == 'reject':
        await query.message.delete()
        await bot.send_message(
            int(from_user),
            f'Your submission for indexing {chat} has been declined by our moderators.',
            reply_to_message_id=int(lst_msg_id)
        )
        return

    if lock.locked():
        return await query.answer('Wait until the previous process completes.', show_alert=True)

    msg = query.message
    await query.answer('Processing...⏳', show_alert=True)

    if int(from_user) not in ADMINS:
        await bot.send_message(
            int(from_user),
            f'Your submission for indexing {chat} has been accepted by our moderators and will be added soon.',
            reply_to_message_id=int(lst_msg_id)
        )

    await msg.edit(
        "Starting Indexing",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton('Cancel', callback_data='index_cancel')]]
        )
    )

    try:
        chat = int(chat)
    except ValueError:
        pass

    await index_files_to_db(int(lst_msg_id), chat, msg, bot)


@Client.on_message(
    (filters.forwarded | filters.regex(r"(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$"))
    & filters.text & filters.private & filters.incoming
)
async def send_for_index(bot, message):
    if message.text:
        regex = re.compile(r"(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        match = regex.match(message.text)
        if not match:
            return await message.reply('Invalid link')

        chat_id = match.group(4)
        last_msg_id = int(match.group(5))
        if chat_id.isnumeric():
            chat_id = int("-100" + chat_id)
    elif message.forward_from_chat and message.forward_from_chat.type == enums.ChatType.CHANNEL:
        last_msg_id = message.forward_from_message_id
        chat_id = message.forward_from_chat.username or message.forward_from_chat.id
    else:
        return

    try:
        await bot.get_chat(chat_id)
    except ChannelInvalid:
        return await message.reply('This may be a private channel/group. Make me an admin there to index files.')
    except (UsernameInvalid, UsernameNotModified):
        return await message.reply('Invalid link specified.')
    except Exception as e:
        logger.exception(e)
        return await message.reply(f'Error - {e}')

    try:
        k = await bot.get_messages(chat_id, last_msg_id)
    except:
        return await message.reply('Make sure I am an admin in the channel if it is private.')

    if k.empty:
        return await message.reply('This may be a group and I am not an admin.')

    if message.from_user.id in ADMINS:
        buttons = [[
            InlineKeyboardButton('Yes', callback_data=f'index#accept#{chat_id}#{last_msg_id}#{message.from_user.id}')
        ], [
            InlineKeyboardButton('Close', callback_data='close_data')
        ]]
        return await message.reply(
            f'Do you want to index this channel/group?\n\nChat ID/Username: <code>{chat_id}</code>\nLast Message ID: <code>{last_msg_id}</code>',
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    if isinstance(chat_id, int):
        try:
            link = (await bot.create_chat_invite_link(chat_id)).invite_link
        except ChatAdminRequired:
            return await message.reply('I need permission to create invite links in the channel.')
    else:
        link = f"@{message.forward_from_chat.username}"

    buttons = [[
        InlineKeyboardButton('Accept Index', callback_data=f'index#accept#{chat_id}#{last_msg_id}#{message.from_user.id}')
    ], [
        InlineKeyboardButton('Reject Index', callback_data=f'index#reject#{chat_id}#{message.id}#{message.from_user.id}')
    ]]

    await bot.send_message(
        LOG_CHANNEL,
        f'#IndexRequest\n\nBy: {message.from_user.mention} (<code>{message.from_user.id}</code>)\nChat ID/Username: <code>{chat_id}</code>\nLast Message ID: <code>{last_msg_id}</code>\nInvite Link: {link}',
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    await message.reply('Thanks for your contribution! Wait for moderators to verify the files.')


@Client.on_message(filters.command('setskip') & filters.user(ADMINS))
async def set_skip_number(bot, message):
    if ' ' in message.text:
        _, skip = message.text.split(" ", 1)
        try:
            skip = int(skip)
            temp.CURRENT = skip
            await message.reply(f"Successfully set SKIP number to {skip}")
        except ValueError:
            await message.reply("Skip number must be an integer.")
    else:
        await message.reply("Usage: /setskip <number>")


async def index_files_to_db(lst_msg_id, chat, msg, bot):
    total_files = 0
    duplicate = 0
    errors = 0
    deleted = 0
    no_media = 0
    unsupported = 0

    async with lock:
        try:
            current = temp.CURRENT
            temp.CANCEL = False

            async for message in bot.iter_messages(chat, lst_msg_id, temp.CURRENT):
                if temp.CANCEL:
                    break

                current += 1

                if current % 60 == 0:
                    await msg.edit_text(
                        f"Fetched: <code>{current}</code>\nSaved: <code>{total_files}</code>\nDuplicates: <code>{duplicate}</code>\nDeleted: <code>{deleted}</code>\nNon-Media Skipped: <code>{no_media + unsupported}</code> (Unsupported: {unsupported})\nErrors: <code>{errors}</code>",
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Cancel', callback_data='index_cancel')]])
                    )

                if message.empty:
                    deleted += 1
                    continue

                if not message.media:
                    no_media += 1
                    continue

                if message.media not in [
                    enums.MessageMediaType.VIDEO,
                    enums.MessageMediaType.AUDIO,
                    enums.MessageMediaType.DOCUMENT
                ]:
                    unsupported += 1
                    continue

                try:
                    wrapped_media = MediaWrapper(message)
                    ok, result = await save_file(wrapped_media)
                    if ok:
                        total_files += 1
                    elif result == 0:
                        duplicate += 1
                    elif result == 2:
                        errors += 1
                except Exception as e:
                    logger.exception(f"Error saving media: {e}")
                    errors += 1

        except Exception as e:
            logger.exception(f"Indexing error: {e}")
            await msg.edit(f'Error occurred: {e}')
        else:
            await msg.edit(
                f"✅ Indexing Complete!\n\nSaved: <code>{total_files}</code>\nDuplicates: <code>{duplicate}</code>\nDeleted: <code>{deleted}</code>\nNon-Media Skipped: <code>{no_media + unsupported}</code> (Unsupported: {unsupported})\nErrors: <code>{errors}</code>"
            )
