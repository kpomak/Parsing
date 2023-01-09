from pymongo import MongoClient
from dotenv import load_dotenv
import os


load_dotenv()
client = MongoClient(
    f'mongodb://{os.environ.get("MONGO_USER")}:{os.environ.get("MONGO_PASSWORD")}@localhost:27017/'
)
print(client.list_database_names())
