# database/connections_mdb.py

from info import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(MONGO_URL)
conn_db = client.auto_filter_db  # ✅ this is what you're importing elsewhere

connect_collection = conn_db.connections


# Save connection
async def add_connection(user_id: int, chat_id: int):
    await connect_collection.update_one(
        {"user_id": user_id},
        {"$addToSet": {"connections": chat_id}},
        upsert=True
    )


# Get all connections for a user
async def get_connections(user_id: int) -> list:
    user_data = await connect_collection.find_one({"user_id": user_id})
    return user_data.get("connections", []) if user_data else []


# Delete a single connection
async def delete_connection(user_id: int, chat_id: int):
    await connect_collection.update_one(
        {"user_id": user_id},
        {"$pull": {"connections": chat_id}}
    )


# Delete all connections
async def delete_all_connections(user_id: int):
    await connect_collection.delete_one({"user_id": user_id})
