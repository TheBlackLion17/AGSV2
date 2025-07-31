import motor.motor_asyncio
from info import MONGO_URL

# Create MongoDB client
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.AutoFilterBotDB  # Use your actual DB name here

# Collection for users
user_collection = db.users
chat_collection = db.chats

class UsersChatsDB:
    def __init__(self):
        self.user_col = user_collection
        self.chat_col = chat_collection

    async def is_user_exist(self, user_id: int) -> bool:
        return await self.user_col.find_one({"user_id": user_id}) is not None

    async def add_user(self, user_id: int):
        if not await self.is_user_exist(user_id):
            await self.user_col.insert_one({"user_id": user_id})

    async def total_users_count(self) -> int:
        return await self.user_col.count_documents({})

    async def get_all_users(self):
        return [doc["user_id"] async for doc in self.user_col.find({}, {"user_id": 1})]

    async def delete_user(self, user_id: int):
        await self.user_col.delete_one({"user_id": user_id})

    # ---------- Chats -----------
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


# Export as userdb
userdb = UsersChatsDB()
