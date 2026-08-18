import db.toastops as toastops
import db.scops as scops
import db.plops as plops
from db.model import Toast, Player, Scoresheet
import utils.anal as anal
import datetime

async def add_player(player: Player):
    """
    Add a player to the database
    """
    id = await plops.add_player(player)
    return str(id)

async def get_players(played_since: int | None = None):
    """
    Retrieve all players; optionally filter by recency
    """
    players = await plops.get_players(played_since)
    for i in range(len(players)):
        players[i] = Player.model_validate(players[i])

    return players