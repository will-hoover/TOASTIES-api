"""
Mongo database connection file
"""

import pymongo
from dotenv import load_dotenv
from db.model import *
from bson import ObjectId

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

def get_last_toast(content: str):
    """
    Retrieve the number of the latest toast 
    """
    client, db = connect()
    toasts = db[TOASTS]
    pipeline = [
        {"$match": {
            "content": content
        }},
        {"$group": {
            "_id": "$content",
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
    client, db = connect()
    toasts = db[TOASTS]
    new = new.model_dump(by_alias=True, exclude_none=True)
    result = toasts.insert_one(new)
    client.close()
    return result.inserted_id

def get_live_toast() -> Toast:
    """
    Return the current toast.
    """
    client, db = connect()
    toasts = db[TOASTS]
    filter = {
        "live": True
    }
    live_toast = toasts.find_one(filter)
    client.close()
    return live_toast

def end_toast(id: str) -> bool:
    """
    End the specified toast
    """
    client, db = connect()
    toasts = db[TOASTS]
    result = toasts.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"live": False}}
    )
    client.close()
    return result.matched_count == 1

if __name__ == "__main__":
    client, db = connect()
    db.create_collection()
    client.close()
    print("Success")