# database/users_chats_db.py

import motor.motor_asyncio
from info import (
    DATABASE_NAME,
    DATABASE_URL,
    IMDB,
    IMDB_TEMPLATE,
    MELCOW_NEW_USERS,
    P_TTI_SHOW_OFF,
    SINGLE_BUTTON,
    SPELL_CHECK_REPLY,
    PROTECT_CONTENT,
)

class Database:

    def __init__(self, uri, db_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[db_name]
        self.users = self.db.users
        self.groups = self.db.groups

    def _new_user(self, user_id, name):
        return {
            "id": user_id,
            "name": name,
            "ban_status": {"is_banned": False, "ban_reason": ""}
        }

    def _new_group(self, chat_id, title, username):
        return {
            "id": chat_id,
            "title": title,
            "username": username,
            "chat_status": {"is_disabled": False, "reason": ""}
        }

    async def add_user(self, user_id, name):
        if not await self.users.find_one({"id": user_id}):
            await self.users.insert_one(self._new_user(user_id, name))

    async def add_chat(self, chat_id, title, username):
        if not await self.groups.find_one({"id": chat_id}):
            await self.groups.insert_one(self._new_group(chat_id, title, username))

    async def is_user_exist(self, user_id):
        return await self.users.find_one({"id": user_id}) is not None

    async def ban_user(self, user_id, reason="No Reason"):
        await self.users.update_one(
            {"id": user_id},
            {"$set": {"ban_status": {"is_banned": True, "ban_reason": reason}}}
        )

    async def remove_ban(self, user_id):
        await self.users.update_one(
            {"id": user_id},
            {"$set": {"ban_status": {"is_banned": False, "ban_reason": ""}}}
        )

    async def get_ban_status(self, user_id):
        user = await self.users.find_one({"id": user_id})
        return user.get("ban_status", {"is_banned": False, "ban_reason": ""}) if user else {"is_banned": False, "ban_reason": ""}

    async def disable_chat(self, chat_id, reason="No Reason"):
        await self.groups.update_one(
            {"id": chat_id},
            {"$set": {"chat_status": {"is_disabled": True, "reason": reason}}}
        )

    async def re_enable_chat(self, chat_id):
        await self.groups.update_one(
            {"id": chat_id},
            {"$set": {"chat_status": {"is_disabled": False, "reason": ""}}}
        )

    async def get_chat_status(self, chat_id):
        chat = await self.groups.find_one({"id": chat_id})
        return chat.get("chat_status") if chat else None

    async def update_settings(self, chat_id, settings: dict):
        await self.groups.update_one({"id": chat_id}, {"$set": {"settings": settings}})

    async def get_settings(self, chat_id):
        default_settings = {
            "button": SINGLE_BUTTON,
            "botpm": P_TTI_SHOW_OFF,
            "file_secure": PROTECT_CONTENT,
            "imdb": IMDB,
            "spell_check": SPELL_CHECK_REPLY,
            "welcome": MELCOW_NEW_USERS,
            "template": IMDB_TEMPLATE,
        }
        chat = await self.groups.find_one({"id": chat_id})
        return chat.get("settings", default_settings) if chat else default_settings

    async def total_users_count(self):
        return await self.users.count_documents({})

    async def total_chat_count(self):
        return await self.groups.count_documents({})

    async def get_all_users(self):
        return self.users.find({})

    async def get_all_chats(self):
        return self.groups.find({})

    async def delete_user(self, user_id):
        await self.users.delete_many({"id": user_id})

    async def delete_chat(self, chat_id):
        await self.groups.delete_many({"id": chat_id})

    async def get_banned(self):
        banned_users = [u["id"] async for u in self.users.find({"ban_status.is_banned": True})]
        banned_chats = [g["id"] async for g in self.groups.find({"chat_status.is_disabled": True})]
        return banned_users, banned_chats

    async def get_db_size(self):
        stats = await self.db.command("dbstats")
        return stats.get("dataSize", 0)


# Global DB Instance
db = Database(DATABASE_URL, DATABASE_NAME)
