import os
from motor.motor_asyncio import AsyncIOMotorClient
from info import MONGO_URL, DB_NAME

class UsersChatsDB:
    def __init__(self, uri=MONGO_URL, database_name=DB_NAME):
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[database_name]

        self.user_col = self.db["users"]
        self.chat_col = self.db["chats"]
        self.bannedList = self.db["bannedList"]

    # ---------- Users ----------
    async def is_user_exist(self, user_id: int) -> bool:
        return await self.user_col.find_one({"user_id": user_id}) is not None

    async def add_user(self, message):
        user = message.from_user

        user_data = {
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "language_code": user.language_code,
            "is_premium": user.is_premium,
            "last_active": message.date
        }

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
