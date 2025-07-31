# database/users_chats_db.py

from motor.motor_asyncio import AsyncIOMotorClient
from info import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client.auto_filter_db  # Use consistent DB name (lowercase, snake_case)

class UserDB:
    def __init__(self):
        self.user_col = db.users
        self.chat_col = db.chats

    async def add_user(self, user_id: int, first_name: str):
        if not await self.user_col.find_one({"_id": user_id}):
            await self.user_col.insert_one({"_id": user_id, "first_name": first_name})

    async def is_user(self, user_id: int) -> bool:
        return await self.user_col.find_one({"_id": user_id}) is not None

    async def get_all_users(self) -> list:
        return await self.user_col.find().to_list(None)

    async def remove_user(self, user_id: int):
        await self.user_col.delete_one({"_id": user_id})

    async def add_chat(self, chat_id: int, title: str):
        if not await self.chat_col.find_one({"_id": chat_id}):
            await self.chat_col.insert_one({"_id": chat_id, "title": title})

    async def is_chat(self, chat_id: int) -> bool:
        return await self.chat_col.find_one({"_id": chat_id}) is not None

    async def get_all_chats(self) -> list:
        return await self.chat_col.find().to_list(None)

    async def remove_chat(self, chat_id: int):
        await self.chat_col.delete_one({"_id": chat_id})

# Export instance
db_instance = UserDB()
