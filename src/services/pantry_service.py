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