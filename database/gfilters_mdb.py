# database/gfilters_mdb.py

from motor.motor_asyncio import AsyncIOMotorClient
from info import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client.auto_filter_db  # Use consistent DB name

global_filters = db.global_filters


# Save or update a global filter
async def save_gfilter(keyword: str, file_data: dict):
    await global_filters.update_one(
        {"keyword": keyword},
        {"$set": {"file_data": file_data}},
        upsert=True
    )


# Get a global filter by keyword
async def get_gfilter(keyword: str) -> dict:
    gfilter = await global_filters.find_one({"keyword": keyword})
    return gfilter.get("file_data") if gfilter else None


# Get all global filter keywords
async def get_all_gfilters() -> list:
    cursor = global_filters.find({})
    return [doc["keyword"] async for doc in cursor]


# Delete a global filter by keyword
async def delete_gfilter(keyword: str):
    await global_filters.delete_one({"keyword": keyword})


# Delete all global filters
async def delete_all_gfilters():
    await global_filters.delete_many({})
