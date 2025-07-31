from pyrogram import Client, idle
import logging
import asyncio
from info import API_ID, API_HASH, BOT_TOKEN, BOT_USERNAME, PLUGINS, LOG_CHANNEL

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

LOGGER = logging.getLogger(__name__)

app = Client(
    name=BOT_USERNAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins={"root": PLUGINS}
)

async def start_bot():
    bot_started = False
    try:
        await app.start()
        bot_started = True  # Mark that app.start() succeeded

        bot_info = await app.get_me()
        LOGGER.info(f"Bot Started as @{bot_info.username} [ID: {bot_info.id}]")

        await app.send_message(
            chat_id=LOG_CHANNEL,
            text=f"✅ **Bot Started Successfully**\n\n👤 **Username:** @{bot_info.username}\n🆔 **User ID:** `{bot_info.id}`"
        )

        await idle()

    except Exception as e:
        LOGGER.error(f"❌ Error while starting bot: {e}")

    finally:
        if bot_started:  # Only stop if it was started
            await app.stop()
            LOGGER.info("Bot Stopped.")

if __name__ == "__main__":
    asyncio.run(start_bot())
