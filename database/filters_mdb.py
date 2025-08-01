import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import enums
from info import DATABASE_URL, DATABASE_NAME

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = AsyncIOMotorClient(DATABASE_URL)
mydb = client[DATABASE_NAME]  # Use your DB name

# Add or update filter
async def add_filter(grp_id, text, reply_text, btn, file, alert):
    try:
        mycol = mydb[str(grp_id)]
        data = {
            'text': str(text),
            'reply': str(reply_text),
            'btn': str(btn),
            'file': str(file),
            'alert': str(alert)
        }
        await mycol.update_one({'text': str(text)}, {"$set": data}, upsert=True)
    except Exception as e:
        logger.error(f"Failed to add filter: {e}")

# Find a filter
async def find_filter(group_id, name):
    try:
        mycol = mydb[str(group_id)]
        result = await mycol.find_one({"text": name})
        if result:
            return (
                result.get('reply'),
                result.get('btn'),
                result.get('alert'),
                result.get('file')
            )
    except Exception as e:
        logger.error(f"Error in find_filter: {e}")
    return None, None, None, None

# Get all filters
async def get_filters(group_id):
    mycol = mydb[str(group_id)]
    filters = []
    async for item in mycol.find({}, {"text": 1, "_id": 0}):
        filters.append(item['text'])
    return filters

# Delete a specific filter
async def delete_filter(message, text, group_id):
    mycol = mydb[str(group_id)]
    query = {'text': text}
    count = await mycol.count_documents(query)
    if count:
        await mycol.delete_one(query)
        await message.reply_text(
            f"`{text}` deleted. I will not respond to that filter anymore.",
            quote=True,
            parse_mode=enums.ParseMode.MARKDOWN
        )
    else:
        await message.reply_text("Couldn't find that filter!", quote=True)

# Delete all filters
async def del_all(message, group_id, title):
    mycol = mydb[str(group_id)]
    try:
        await mycol.drop()
        await message.edit_text(f"All filters from {title} have been removed.")
    except Exception as e:
        logger.error(f"Failed to drop collection: {e}")
        await message.edit_text("Couldn't remove all filters from group!")

# Count number of filters
async def count_filters(group_id):
    try:
        mycol = mydb[str(group_id)]
        return await mycol.count_documents({})
    except Exception as e:
        logger.error(f"Error counting filters: {e}")
        return 0

# Global filter stats
async def filter_stats():
    total_count = 0
    total_groups = 0
    try:
        for collection_name in await mydb.list_collection_names():
            if collection_name != "CONNECTION":
                count = await mydb[collection_name].count_documents({})
                total_count += count
                total_groups += 1
    except Exception as e:
        logger.error(f"Error in filter_stats: {e}")
    return total_groups, total_count
