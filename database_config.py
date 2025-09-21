from settings import settings
from pymongo import AsyncMongoClient


MONGO_URI = settings.MONGO_URI
client = AsyncMongoClient(MONGO_URI)

# DATA BASES
MATHS_QA_DB_NAME = "maths-q-a"

# COLLECTIONS
QANDA_COLLECTION = client[MATHS_QA_DB_NAME]["qanda"]
CONVERSATION_COLLECTION = client[MATHS_QA_DB_NAME]["conversations"]


# async def test_db_connection():
#     try:
#         # The ismaster command is cheap and does not require auth.
#         await client.admin.command('ismaster')
#         print("MongoDB connection successful")
#     except Exception as e:
#         print(f"MongoDB connection error: {e}")

#     # printinf databases
#     dbs = await client.list_database_names()
#     print("Databases:", dbs)
#     # printing collections in the database
#     collections = await client[MATHS_QA_DB_NAME].list_collection_names()
#     print("Collections in maths-q-a database:", collections)
#     # two records from the collection
#     records = await QANDA_COLLECTION.find().to_list(2)
#     print("Sample records from qanda collection:", records)

# # Call the test function
# import asyncio
# asyncio.run(test_db_connection())
