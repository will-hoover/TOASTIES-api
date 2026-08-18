"""
Scoresheet mongodb operations
"""

from db.model import Scoresheet
from db.db import db
from bson import ObjectId

SCORESHEETS = "Scoresheets"

async def add_scoresheet(s: Scoresheet):
    """
    Add a scoresheet to the database
    """
    sc = db[SCORESHEETS]
    s = s.model_dump(by_alias=True, exclude_none=True)
    result = await sc.insert_one(s)
    return result.inserted_id

async def check_scoresheet_present(s: Scoresheet):
    """
    Checks if the given scoresheet metadata is present and if so, returns the scoresheet id.
    """
    sc = db[SCORESHEETS]
    filter = {
        "toast": s.toast,
        "room": s.room,
        "writer": s.writer
    }
    result = await sc.find_one(filter)
    if result is None:
        return None
    return result["_id"]

async def update_scoresheet(id: ObjectId, s: Scoresheet):
    """
    Update certain scoresheet metadata at the given id
    """
    sc = db[SCORESHEETS]
    result = await sc.update_one(
            {"_id": id},
            {"$set": {"questions": s.questions}}
        )
    return result.matched_count

async def get_scoresheets_by_toast(
    toast: str | None = None, 
    room: int | None = None
):
    """
    Retrieve all scoresheets filtered by the specified toast and room if provided.
    """
    sc = db[SCORESHEETS]
    filter = {}
    if toast != None:
        filter["toast"] = toast
    if room != None:
        filter["room"] = room

    result = await sc.find(filter).to_list()
    return result

async def get_last_scoresheet(toast: str, room: int):
    """
    Get the scoresheet for the previous packet in this room
    """
    sc = db[SCORESHEETS]
    filter = {
        "toast": toast,
        "room": room
    }
    result = await sc.find(filter).sort({"timestamp": -1}).limit(1).to_list()
    return result