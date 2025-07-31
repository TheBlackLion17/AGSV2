import os
from motor.motor_asyncio import AsyncIOMotorClient
from info import MONGO_URL, DB_NAME  # Make sure DB_NAME is defined in info.py

class UsersChatsDB:
    def __init__(self, uri=None, database_name=None):
        uri = uri or MONGO_URL
        database_name = database_name or DB_NAME

        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[database_name]

        # Collection references
        self.user_col = self.db["users"]
        self.chat_col = self.db["chats"]
        self.bannedList = self.db["bannedList"]

    # ---------- Users ----------
    async def is_user_exist(self, user_id: int) -> bool:
        return await self.user_col.find_one({"user_id": user_id}) is not None

    async def add_user(self, user_id: int, name: str):
        await self.user_col.update_one(
            {"user_id": user_id},
            {"$set": {"user_id": user_id, "name": name}},
            upsert=True
        )

    async def total_users_count(self) -> int:
        return await self.user_col.count_documents({})

    async def get_all_users(self):
        return [doc["user_id"] async for doc in self.user_col.find({}, {"user_id": 1})]

    async def delete_user(self, user_id: int):
        await self.user_col.delete_one({"user_id": user_id})

    # ---------- Chats ----------
    async def is_chat_exist(self, chat_id: int) -> bool:
        return await self.chat_col.find_one({"chat_id": chat_id}) is not None

    async def add_chat(self, chat_id: int):
        if not await self.is_chat_exist(chat_id):
            await self.chat_col.insert_one({"chat_id": chat_id})

    async def get_all_chats(self):
        return [doc["chat_id"] async for doc in self.chat_col.find({}, {"chat_id": 1})]

    async def total_chat_count(self) -> int:
        return await self.chat_col.count_documents({})

    async def delete_chat(self, chat_id: int):
        await self.chat_col.delete_one({"chat_id": chat_id})

# ✅ Create reusable instance
userdb = UsersChatsDB()
