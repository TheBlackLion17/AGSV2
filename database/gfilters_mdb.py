import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import enums
from info import DATABASE_URL, DATABASE_NAME

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = AsyncIOMotorClient(DATABASE_URL)
mydb = client[DATABASE_NAME]  # "GlobalFilters"

# Add or update a global filter
async def add_gfilter(gfilters, text, reply_text, btn, file, alert):
    try:
        mycol = mydb[str(gfilters)]
        data = {
            'text': str(text),
            'reply': str(reply_text),
            'btn': str(btn),
            'file': str(file),
            'alert': str(alert)
        }
        await mycol.update_one({'text': str(text)}, {"$set": data}, upsert=True)
    except Exception as e:
        logger.error(f"Error in add_gfilter: {e}")

# Find a global filter
async def find_gfilter(gfilters, name):
    try:
        mycol = mydb[str(gfilters)]
        result = await mycol.find_one({"text": name})
        if result:
            return (
                result.get('reply'),
                result.get('btn'),
                result.get('alert'),
                result.get('file')
            )
    except Exception as e:
        logger.error(f"Error in find_gfilter: {e}")
    return None, None, None, None

# Get all global filters
async def get_gfilters(gfilters):
    mycol = mydb[str(gfilters)]
    filters = []
    try:
        async for item in mycol.find({}, {"text": 1, "_id": 0}):
            filters.append(item['text'])
    except Exception as e:
        logger.error(f"Error in get_gfilters: {e}")
    return filters

# Delete a specific global filter
async def delete_gfilter(message, text, gfilters):
    mycol = mydb[str(gfilters)]
    try:
        query = {'text': text}
        count = await mycol.count_documents(query)
        if count:
            await mycol.delete_one(query)
            await message.reply_text(
                f"`{text}` deleted. I will not respond to that global filter anymore.",
                quote=True,
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await message.reply_text("Couldn't find that global filter!", quote=True)
    except Exception as e:
        logger.error(f"Error in delete_gfilter: {e}")

# Delete all global filters from a specific group
async def del_allg(message, gfilters):
    try:
        if str(gfilters) not in await mydb.list_collection_names():
            await message.edit_text("Nothing to remove!")
            return
        await mydb[str(gfilters)].drop()
        await message.edit_text("All global filters have been removed.")
    except Exception as e:
        logger.error(f"Error in del_allg: {e}")
        await message.edit_text("Couldn't remove all filters!")

# Count number of global filters in a group
async def count_gfilters(gfilters):
    try:
        count = await mydb[str(gfilters)].count_documents({})
        return count if count else False
    except Exception as e:
        logger.error(f"Error in count_gfilters: {e}")
        return False

# Get stats across all global filter groups
async def gfilter_stats():
    totalcount = 0
    try:
        collections = await mydb.list_collection_names()
        if "CONNECTION" in collections:
            collections.remove("CONNECTION")

        for collection in collections:
            count = await mydb[collection].count_documents({})
            totalcount += count

        return len(collections), totalcount
    except Exception as e:
        logger.error(f"Error in gfilter_stats: {e}")
        return 0, 0
