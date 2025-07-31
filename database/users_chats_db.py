import motor.motor_asyncio
import os
from dotenv import load_dotenv
from info import MONGO_URL


load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.AutoFilterDB

class UserDB:
    def __init__(self):
        self.user_col = db.users
        self.chat_col = db.chats

    async def add_user(self, user_id: int, first_name: str):
        user = await self.user_col.find_one({"_id": user_id})
        if not user:
            await self.user_col.insert_one({"_id": user_id, "first_name": first_name})

    async def is_user(self, user_id: int):
        return await self.user_col.find_one({"_id": user_id}) is not None

    async def get_all_users(self):
        return await self.user_col.find().to_list(None)

    async def add_chat(self, chat_id: int, title: str):
        chat = await self.chat_col.find_one({"_id": chat_id})
        if not chat:
            await self.chat_col.insert_one({"_id": chat_id, "title": title})

    async def get_all_chats(self):
        return await self.chat_col.find().to_list(None)

    async def is_chat(self, chat_id: int):
        return await self.chat_col.find_one({"_id": chat_id}) is not None

    async def remove_user(self, user_id: int):
        await self.user_col.delete_one({"_id": user_id})

    async def remove_chat(self, chat_id: int):
        await self.chat_col.delete_one({"_id": chat_id})


userdb = UserDB()
