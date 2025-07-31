class script:
    START_TXT = """👋 Hello [{}](tg://user?id={})!
    
I am an advanced AutoFilter Bot with:

• Auto/manual filters  
• File renaming & indexing  
• IMDB/TMDB search  
• Admin commands  
• MongoDB support  
• User & group controls  
• Force subscription  

Use the buttons below to explore all features."""

    HELP_TXT = """
🔹 **Help Menu**

➤ `Filter Commands:`
• /filter [name] - Add new filter
• /filters - List filters
• /del [name] - Delete filter
• /delall - Delete all

➤ `Admin Commands:`
• /stats - DB stats
• /logs - Error logs
• /restart - Restart bot
• /update - Pull updates
• /ban_user [ID] - Ban user
• /unban_user [ID] - Unban user

➤ `User Commands:`
• /id - Get ID
• /info - File/Chat info
• /settings - Manage settings
• /leave - Make bot leave group

➤ `Indexing:`
• /delete [ID] - Delete file
• /deleteall - Wipe DB

⚙️ Need more help? Join @YourSupportGroup
"""

    ABOUT_TXT = """
🤖 **Bot Name:** AutoFilter V5  
🧑‍💻 **Developer:** @YourUsername  
📚 **Library:** [Pyrogram](https://docs.pyrogram.org/)  
🗃 **Database:** MongoDB  
🖥 **Hosted On:** VPS  
🔐 **License:** MIT  
"""

    BANNED_USER_TEXT = "🚫 You are banned from using this bot. Contact the admin."
    
    FORCE_SUB_TEXT = """🚫 To use this bot, you must join our updates channel!

Click the button below and join the channel. Then press `✅ Joined`."""
    
    WELCOME_TEXT = "👋 Welcome to the group, {}!"
    
    FILTER_ADDED = "✅ Filter '{}' added successfully!"
    FILTER_DELETED = "🗑 Filter '{}' deleted!"
    NO_FILTERS = "⚠️ No filters found."
    FILTERS_CLEARED = "🧹 All filters have been cleared."

    FILE_RENAMED = "✅ File renamed successfully!"
    FILE_INDEXED = "📁 File has been added to database."

    ADMIN_ONLY = "❌ This command is only for admins."

    ERROR_TEXT = "⚠️ Something went wrong. Try again later or check logs."

    UPLOADING_MSG = "📤 Uploading your file..."
    DOWNLOADING_MSG = "📥 Downloading media..."
    COMPRESSING_MSG = "🗜 Compressing..."
    PROGRESS_MSG = "⏳ Processing..."

