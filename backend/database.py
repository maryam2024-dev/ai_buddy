
from motor.motor_asyncio import AsyncIOMotorClient # type: ignore
from utils.load_helper import DATABASE_HOST,DATABASE_NAME




client = AsyncIOMotorClient(DATABASE_HOST)
# data database
database = client[DATABASE_NAME]
user_collection=database.users











async def check_connection():
    try:
        await client.admin.command('ping')
        print("Connection to mongodb database!")
        return True
    except Exception as e:
        print("Failed to connect to MongoDB:", e)
        return False
    