import db.toastops as toastops
import db.scops as scops
from db.model import Toast, Scoresheet
import utils.anal as anal
import datetime

async def start_toast(toast: Toast):
    """
    Start the next toast for trash or academic day
    """
    last_toast = await toastops.get_last_toast(toast.content)
    if toast.number != None and toast.number <= last_toast[0]["lastNum"]:
        return -1
    toast.date = datetime.datetime.now()
    toast.live = True
    id = await toastops.insert_toast(toast)
    return id

async def get_live_toast():
    """
    Get the number and day type from 
    """
    live = await toastops.get_live_toast()
    if live is not None:
        return Toast.model_validate(live)

async def end_toast(id: str) -> int:
    """
    End the specified toast if it is live
    """
    live = await toastops.get_live_toast()
    if live is None or id != Toast.model_validate(live).id:
        return -1
    updated = await toastops.end_toast(id)
    if updated:
        return 1
    return 0

async def get_rooms(id: str) -> int:
    """
    Get the number of rooms for the specified toast
    """
    result = await toastops.get_rooms(id)
    if len(result) == 0:
        return None
    return result[0]['rooms']

async def add_room(id: str) -> int:
    """
    Add a room to the specified toast
    """
    live = await toastops.get_live_toast()
    if live is None or id != Toast.model_validate(live).id:
        return -1
    updated = await toastops.add_room(id)
    if updated:
        return 1
    return 0

async def add_scoresheet(scoresheet: Scoresheet) -> int:
    """
    Add a scoresheet to the database
    """
    live = await toastops.get_live_toast()
    if live is None or scoresheet.toast != Toast.model_validate(live).id:
        return -1
    prev_id = await scops.check_scoresheet_present(scoresheet)
    if prev_id != None:
        await scops.update_scoresheet(prev_id, scoresheet)
        return 1
    id = await scops.add_scoresheet(scoresheet)
    if id is None:
        return 0
    return 1

async def get_stats(toast: str | None = None, room: int | None = None):
    """
    Obtain a live stats report
    """
    if toast == None:
        live = await toastops.get_live_toast()
        if live is None:
                return None
        toast = Toast.model_validate(live).id

    scoresheets = await scops.get_scoresheets_by_toast(toast, room)
    if len(scoresheets) == 0:
        return dict()
    for i in range(len(scoresheets)):
        scoresheets[i] = Scoresheet.model_validate(scoresheets[i])
    return anal.compile_stats(scoresheets)

async def get_last_roster(room: int):
    """
    Get the roster for the most recent game in the specified toast/room
    """
    live = await toastops.get_live_toast()
    if live is None:
            return None
    toast = Toast.model_validate(live).id

    last_sc = await scops.get_last_scoresheet(toast, room)
    if len(last_sc) == 0:
        return None
    return Scoresheet.model_validate(last_sc[0]).roster
