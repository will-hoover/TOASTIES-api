import db.mongops as mongops
from db.model import Toast, Player, Scoresheet
import datetime

def start_toast(toast: Toast):
    """
    Start the next toast for trash or academic day
    """
    last_toast = mongops.get_last_toast(toast.content)
    if toast.number != None and toast.number <= last_toast[0]["lastNum"]:
        return -1
    toast.date = datetime.datetime.now()
    toast.live = True
    id = mongops.insert_toast(toast)
    return id

def get_live_toast():
    """
    Get the number and day type from 
    """
    live = mongops.get_live_toast()
    if live is not None:
        return Toast.model_validate(live)

def end_toast(id: str) -> int:
    """
    End the specified toast if it is live
    """
    live = mongops.get_live_toast()
    if live is None or id != Toast.model_validate(live).id:
        return -1
    updated = mongops.end_toast(id)
    if updated:
        return 1
    return 0

def get_rooms(id: str) -> int:
    """
    Get the number of rooms for the specified toast
    """
    result = mongops.get_rooms(id)
    return result['rooms']

def add_room(id: str) -> int:
    """
    Add a room to the specified toast
    """
    live = mongops.get_live_toast()
    if live is None or id != Toast.model_validate(live).id:
        return -1
    updated = mongops.add_room(id)
    if updated:
        return 1
    return 0