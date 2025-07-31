import os
import asyncio
from datetime import datetime
from pytz import timezone

from pyrogram import __version__
from pyrogram.raw.all import layer
from pyromod import Client
from aiohttp import web

from info import *  # Your info.py should define API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL, etc.
from route import web_server  # Your route/web.py must define async def web_server()

import pyrogram.utils
pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -1009999999999


class Bot(Client):

    def __init__(self):
        super().__init__(
            name="renamer",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()

        self.mention = me.mention
        self.username = me.username
        self.uptime = BOT_UPTIME

        print(f"{me.first_name} is started.....✨")

        # Notify admins
        for admin_id in ADMINS:
            try:
                await self.send_message(admin_id, f"**{me.first_name} is started...**")
            except Exception as e:
                print(f"Error sending message to admin {admin_id}: {e}")

        # Notify log channel
        if LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(
                    LOG_CHANNEL,
                    f"**{me.mention} is Restarted !!**\n\n"
                    f"📅 Date : `{date}`\n"
                    f"⏰ Time : `{time}`\n"
                    f"🌐 Timezone : `Asia/Kolkata`\n\n"
                    f"🉐 Version : `v{__version__} (Layer {layer})`"
                )
            except Exception as e:
                print(f"Error sending message to LOG_CHANNEL: {e}")

        # Start webhook server if enabled
        if WEBHOOK:
            try:
                app = web.AppRunner(await web_server())
                await app.setup()
                PORT = int(os.environ.get("PORT", 8081))
                await web.TCPSite(app, "0.0.0.0", PORT).start()
            except Exception as e:
                print(f"Webhook Error: {e}")

    async def stop(self):
        await super().stop()
        print(f"{self.mention} is stopped.")


bot = Bot()

async def main():
    await bot.start()
    print("Bot is running... (Press Ctrl+C to stop)")
    await asyncio.get_event_loop().create_future()  # Keeps the bot running

try:
    asyncio.run(main())
except (KeyboardInterrupt, SystemExit):
    print("Stopping bot...")
    asyncio.run(bot.stop())
