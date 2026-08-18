"""
Toast object db operations
"""

from db.model import Toast
from db.db import db
from bson import ObjectId

TOASTS = "Toasts"

async def get_last_toast(content: str):
    """
    Retrieve the number of the latest toast 
    """
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
    result = await toasts.aggregate(pipeline).to_list()
    return result

async def insert_toast(new: Toast):
    """
    Insert a new toast into the database
    """
    toasts = db[TOASTS]
    new = new.model_dump(by_alias=True, exclude_none=True)
    result = await toasts.insert_one(new)
    return result.inserted_id

async def get_live_toast() -> Toast:
    """
    Return the current toast.
    """
    toasts = db[TOASTS]
    filter = {
        "live": True
    }
    live_toast = await toasts.find_one(filter)
    return live_toast

async def end_toast(id: str) -> bool:
    """
    End the specified toast
    """
    toasts = db[TOASTS]
    result = await toasts.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"live": False}}
    )
    return result.matched_count == 1

async def get_rooms(id: str) -> int:
    """
    Get the number of rooms in the specified toast
    """
    toasts = db[TOASTS]
    pipeline = [
        {"$match": {
            "_id": ObjectId(id)
        }},
        {"$project": {
            "_id": 0,
            "rooms": 1
        }}
    ]
    result = await toasts.aggregate(pipeline).to_list()
    return result

async def add_room(id: str) -> bool:
    """
    Add a room to the specified toast
    """
    toasts = db[TOASTS]
    result = await toasts.update_one(
        {"_id": ObjectId(id)},
        {"$inc": {"rooms": 1}}
    )
    return result.matched_count == 1

if __name__ == "__main__":
    db.create_collection()
    print("Success")