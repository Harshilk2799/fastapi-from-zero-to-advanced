from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = AsyncIOMotorClient(settings.mongo_uri)
database = client[settings.db_name]
student_collection = database.get_collection("students")