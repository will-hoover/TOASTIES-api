"""
Player mongodb operations
"""

from db.model import Player
from db.db import db
from bson import ObjectId

PLAYERS = "Players"

async def add_player(player: Player):
    """
    Add a player to the system
    """
    players = db[PLAYERS]
    player = player.model_dump(by_alias=True, exclude_none=True)
    result = await players.insert_one(player)
    return result.inserted_id

async def get_players(played_since: int | None = None):
    """
    Get all players, optionally exclude any who haven't played in recent toasts
    """
    players = db[PLAYERS]
    filter = {}
    if played_since != None:
        filter["lastToast"] = {"$gte": played_since}
    result = await players.find(filter).to_list()
    return result