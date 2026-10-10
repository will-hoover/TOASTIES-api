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

async def get_toasts(content: str | None = None):
    """
    Retrieve all toasts; optionally specify trash or academic
    """
    toasts = await toastops.get_toasts(content)
    for i in range(len(toasts)):
        toasts[i] = Toast.model_validate(toasts[i])
    return toasts

async def get_all_stats(content: str):
    """
    Get trash or academic all-time stats
    """
    toasts = await toastops.get_toasts(content)
    ids = [
        Toast.model_validate(t).id for t in toasts
    ]
    scoresheets = await scops.get_scoresheets_from_subset(ids)
    for i in range(len(scoresheets)):
        scoresheets[i] = Scoresheet.model_validate(scoresheets[i])
    return anal.compile_stats(scoresheets)

async def get_player_stats(player: str):
    """
    Get historic stats for a single player
    """
    scoresheets = await scops.get_scoresheets_by_player(player)
    for i in range(len(scoresheets)):
            scoresheets[i] = Scoresheet.model_validate(scoresheets[i])
    return anal.player_stats(player, scoresheets)