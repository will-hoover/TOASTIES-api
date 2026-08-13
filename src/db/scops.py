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