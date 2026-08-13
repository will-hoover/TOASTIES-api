from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
import uvicorn

import services.toasties_service as toasties
from db.model import Scoresheet, Toast

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/toast")
async def current_toast(response: Response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    current = toasties.get_live_toast()
    if current is None:
        raise HTTPException(404, "Buttered Toast is not live. Please start a Toast.")
    return current

@app.post("/start")
async def start_toast(toast: Toast, response: Response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    new_id = toasties.start_toast(toast)
    if new_id == -1:
        raise HTTPException(409, "That Toast already happened!")
    response.status_code = 201
    return { "number": toast.number, "id": str(new_id) }

@app.post("/end/{id}")
async def finish_toast(id: str, response: Response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    code = toasties.end_toast(id)
    if code == -1:
        raise HTTPException(409, "Specified toast is not currently live")
    if code == 0:
        raise HTTPException(500, "Update failed")

@app.get("/rooms/{id}")
async def rooms(id: str, response: Response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    rooms = toasties.get_rooms(id)
    return {
        "rooms": rooms
    }

@app.post("/addroom/{id}")
async def addroom(id: str, response: Response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    code = toasties.add_room(id)
    if code == -1:
        return HTTPException(409, "Cannot add a room to an archived Toast")
    if code == 0:
        return HTTPException(404, "Toast does not exist")
    rooms = toasties.get_rooms(id)
    return {
        "rooms": rooms
    }


@app.get("/stats/{room_number}")
async def room_stats(room_number: int, response: Response):
    # TODO: get stats for the given room number
    pass

@app.get("/combinedstats")
async def combined_stats(response: Response):
    # TODO: get combined stats for all rooms
    pass

@app.post("/submitpacket/{room}")
async def add_scoresheet(room: int, results: Scoresheet, response: Response):
    # TODO: add provided scoresheet to the database
    # TODO: part 2: figure out if we can use the db Scoresheet model for this api call
    pass

@app.get("/roster/{room}")
async def get_last_roster(room: int, response: Response):
    # TODO: get the roster for the most recent game in this room
    pass

@app.post("/loadsheets")
async def load_sheets(ids: dict):
    # We shouldn't need this one
    pass

@app.options("/submitpacket/{room}")
async def submit_preflight(room: int):
    # This is silly API POST stuff I don't quite understand
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': '*'
    }
    return Response(status_code=204, headers=headers)

if __name__ == "__main__":
    uvicorn.run("main:app", log_level="info", reload=True, host="localhost", port=8000)