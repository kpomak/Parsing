import json
import os
from pprint import pprint

from dotenv import load_dotenv
from pymongo import MongoClient

from beautysoup import hh_parse, sj_parse


def collection_updater(target: int, collection: MongoClient) -> None:
    """
    function updates existing records in collection of database
    or adds new records
    """
    print(f"Total records: {collection.count_documents({})}")

    fresh_data = []
    hh_parse(target, fresh_data)
    sj_parse(target, fresh_data)

    print(f"Parsed records: {len(fresh_data)}")

    for doc in fresh_data:
        collection.update_one({"_id": doc["_id"]}, {"$set": doc}, upsert=True)

    print(f"Total records after update: {len(list(collection.find()))}")


def salary_filter(requested_salary: int, collection: MongoClient) -> None:
    """
    function prints vacancies with salary greather than requested value
    """
    for document in collection.find(
        {
            "$or": [
                {"salary.1": {"$gt": requested_salary}},
                {"salary.0": {"$gt": requested_salary}},
                {
                    "$and": [
                        {"salary.1": "infinity"},
                        {"salary.0": {"$lt": requested_salary}},
                    ]
                },
            ]
        }
    ):
        pprint(document)


if __name__ == "__main__":
    load_dotenv()
    client = MongoClient(
        f'mongodb://{os.environ.get("MONGO_USER")}:{os.environ.get("MONGO_PASSWORD")}@localhost:27017/'
    )
    print(f"Список баз данных {client.list_database_names()}")

    db = client.parsers
    collection = db.vacancies
    collection.drop()

    with open("offers.json", "r") as f:
        data = json.load(f)
        collection.insert_many(data)

    collection_updater("Django", collection)
    salary_filter(100000, collection)
