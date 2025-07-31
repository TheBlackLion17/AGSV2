import motor.motor_asyncio
from info import MONGO_URL

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.AutoFilterDB

class LAFilterDB:
    def __init__(self):
        self.la_filters = db.la_filters

    async def add_la_filter(self, name: str, data: dict):
        """Add or update a filter with a name."""
        await self.la_filters.update_one(
            {"name": name},
            {"$set": {"data": data}},
            upsert=True
        )

    async def get_la_filter(self, name: str):
        """Retrieve filter data by name."""
        result = await self.la_filters.find_one({"name": name})
        return result.get("data") if result else None

    async def delete_la_filter(self, name: str):
        """Delete a filter by name."""
        await self.la_filters.delete_one({"name": name})

    async def list_la_filters(self):
        """List all filter names."""
        return [doc["name"] async for doc in self.la_filters.find({}, {"name": 1})]

# Export instance
la_db = LAFilterDB()
