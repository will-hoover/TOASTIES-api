import db.mongops as mongops
from db.model import Toast, Player, Scoresheet
import datetime

def start_toast(toast: Toast):
    """
    Start the next toast for trash or academic day
    """
    last_toast = mongops.get_last_toast(toast.trashDay)
    if toast.number != None and toast.number != last_toast[0]["lastNum"]:
        return -1
    toast.date = datetime.datetime.now()
    id = mongops.insert_toast(toast)
    return id