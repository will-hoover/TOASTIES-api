"""
Mongo database connection file
"""

import pymongo
from dotenv import load_dotenv
from db.model import *

# DB connection variables - change these as required for your local system.
load_dotenv()
 
URI = "mongodb://localhost:27017/"
DB_NAME = "toaster"

TOASTS = "Toasts"

def connect():
    """
    Creates and returns a connection to the mongo db. Must be closed after use.
    """
    client = pymongo.MongoClient(URI)
    db = client[DB_NAME]
    return client, db

def get_last_toast(trash_day: bool):
    """
    Retrieve the number of the latest toast 
    """
    client, db = connect()
    toasts = db[TOASTS]
    pipeline = [
        {"$match": {
            "trashDay": trash_day
        }},
        {"$group": {
            "_id": "$trashDay",
            "lastNum": {"$max": "$number"}
        }}
    ]
    result = toasts.aggregate(pipeline).to_list()
    client.close()
    return result

def insert_toast(new: Toast):
    """
    Insert a new toast into the database
    """
    new = validated_toast(new)
    client, db = connect()
    toasts = db[TOASTS]
    result = toasts.insert_one(new)
    client.close()
    return result.inserted_id


if __name__ == "__main__":
    client, db = connect()
    db.create_collection()
    client.close()
    print("Success")