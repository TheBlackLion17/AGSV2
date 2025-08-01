import logging
from motor.motor_asyncio import AsyncIOMotorClient
from info import DATABASE_URL, DATABASE_NAME

# Logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# MongoDB setup
client = AsyncIOMotorClient(DATABASE_URL)
db = client[DATABASE_NAME]
collection = db['CONNECTION']


async def add_connection(group_id: int, user_id: int) -> bool:
    try:
        user = await collection.find_one({"_id": user_id})
        if user:
            group_ids = [x["group_id"] for x in user.get("group_details", [])]
            if group_id in group_ids:
                return False
            await collection.update_one(
                {"_id": user_id},
                {
                    "$push": {"group_details": {"group_id": group_id}},
                    "$set": {"active_group": group_id}
                }
            )
        else:
            await collection.insert_one({
                "_id": user_id,
                "group_details": [{"group_id": group_id}],
                "active_group": group_id
            })
        return True
    except Exception as e:
        logger.exception("Error in add_connection: %s", e)
        return False


async def active_connection(user_id: int) -> int | None:
    try:
        user = await collection.find_one({"_id": user_id}, {"active_group": 1})
        return int(user["active_group"]) if user and user.get("active_group") else None
    except Exception as e:
        logger.exception("Error in active_connection: %s", e)
        return None


async def all_connections(user_id: int) -> list[int] | None:
    try:
        user = await collection.find_one({"_id": user_id}, {"group_details": 1})
        return [x["group_id"] for x in user.get("group_details", [])] if user else None
    except Exception as e:
        logger.exception("Error in all_connections: %s", e)
        return None


async def if_active(user_id: int, group_id: int) -> bool:
    try:
        user = await collection.find_one({"_id": user_id}, {"active_group": 1})
        return user and user.get("active_group") == group_id
    except Exception as e:
        logger.exception("Error in if_active: %s", e)
        return False


async def make_active(user_id: int, group_id: int) -> bool:
    try:
        result = await collection.update_one({"_id": user_id}, {"$set": {"active_group": group_id}})
        return result.modified_count > 0
    except Exception as e:
        logger.exception("Error in make_active: %s", e)
        return False


async def make_inactive(user_id: int) -> bool:
    try:
        result = await collection.update_one({"_id": user_id}, {"$set": {"active_group": None}})
        return result.modified_count > 0
    except Exception as e:
        logger.exception("Error in make_inactive: %s", e)
        return False


async def delete_connection(user_id: int, group_id: int) -> bool:
    try:
        result = await collection.update_one(
            {"_id": user_id},
            {"$pull": {"group_details": {"group_id": group_id}}}
        )
        if result.modified_count == 0:
            return False

        user = await collection.find_one({"_id": user_id})
        remaining_groups = user.get("group_details", [])
        if not remaining_groups:
            await make_inactive(user_id)
        elif user.get("active_group") == group_id:
            new_active = remaining_groups[-1]["group_id"]
            await make_active(user_id, new_active)

        return True
    except Exception as e:
        logger.exception("Error in delete_connection: %s", e)
        return False
