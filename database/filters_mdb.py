# database/filters_mdb.py

from motor.motor_asyncio import AsyncIOMotorClient
from info import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client.auto_filter_db  # change name if needed

filters_collection = db.filters


# Save a filter
async def save_filter(chat_id: int, keyword: str, file_data: dict):
    await filters_collection.update_one(
        {"chat_id": chat_id, "keyword": keyword},
        {"$set": {"file_data": file_data}},
        upsert=True
    )


# Get a filter by keyword
async def get_filter(chat_id: int, keyword: str) -> dict:
    filter_data = await filters_collection.find_one({"chat_id": chat_id, "keyword": keyword})
    return filter_data.get("file_data") if filter_data else None


# Get all filters for a chat
async def get_all_filters(chat_id: int) -> list:
    cursor = filters_collection.find({"chat_id": chat_id})
    return [doc["keyword"] async for doc in cursor]


# Delete a specific filter
async def delete_filter(chat_id: int, keyword: str):
    await filters_collection.delete_one({"chat_id": chat_id, "keyword": keyword})


# Delete all filters for a chat
async def delete_many_filters(chat_id: int):
    await filters_collection.delete_many({"chat_id": chat_id})


# ✅ Export db object for import in __init__.py
filters_db = db
