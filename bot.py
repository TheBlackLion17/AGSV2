from pyrogram import Client, idle
import logging
from info import API_ID, API_HASH, BOT_TOKEN, BOT_USERNAME, PLUGINS, LOG_CHANNEL

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
LOGGER = logging.getLogger(__name__)

app = Client(
    name=agsv2,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins={"root": PLUGINS}
)

async def main():
    await app.start()
    bot_info = await app.get_me()

    LOGGER.info(f"Bot Started as @{bot_info.username} [ID: {bot_info.id}]")

    # Safe log to channel
    try:
        await app.send_message(
            chat_id=LOG_CHANNEL,
            text=f"✅ **Bot Started Successfully**\n\n👤 **Username:** @{bot_info.username}\n🆔 **User ID:** `{bot_info.id}`"
        )
    except Exception as e:
        LOGGER.warning(f"Could not send log message to LOG_CHANNEL: {e}")

    await idle()
    await app.stop()
    LOGGER.info("Bot Stopped.")

if __name__ == "__main__":
    app.run(main())
