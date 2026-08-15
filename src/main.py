from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from typing import Literal
import uvicorn

import services.toasties_service as toasties
import services.pantry_service as pantry
from db.model import Scoresheet, Toast, Player
from db.db import lifespan

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/toast")
async def current_toast(response: Response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    current = await toasties.get_live_toast()
    if current is None:
        raise HTTPException(404, "Buttered Toast is not live. Please start a Toast.")
    return current

@app.post("/start")
async def start_toast(toast: Toast, response: Response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    new_id = await toasties.start_toast(toast)
    if new_id == -1:
        raise HTTPException(409, "That Toast already happened!")
    response.status_code = 201
    return { "number": toast.number, "id": str(new_id) }

@app.post("/end/{id}")
async def finish_toast(id: str, response: Response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    code = await toasties.end_toast(id)
    if code == -1:
        raise HTTPException(409, "Specified toast is not currently live")
    if code == 0:
        raise HTTPException(500, "Update failed")

@app.get("/rooms/{id}")
async def rooms(id: str, response: Response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    rooms = await toasties.get_rooms(id)
    if rooms is None:
        raise HTTPException(404, "Toast des not exist")
    return {
        "rooms": rooms
    }

@app.post("/addroom/{id}")
async def addroom(id: str, response: Response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    code = await toasties.add_room(id)
    if code == -1:
        raise HTTPException(409, "Cannot add a room to an archived Toast")
    if code == 0:
        raise HTTPException(404, "Toast does not exist")
    rooms = await toasties.get_rooms(id)
    return {
        "rooms": rooms
    }

@app.post("/scoresheet")
async def add_scoresheet(results: Scoresheet, response: Response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    code = await toasties.add_scoresheet(results)
    if code == -1:
        raise HTTPException(409, "Specified Toast is not live")
    response.status_code = 201

@app.get("/stats/{room_number}")
async def room_stats(room_number: int, response: Response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    stats = await toasties.get_live_stats(room_number)
    if stats == None:
        raise HTTPException(404, "Buttered Toast is not live")
    return stats

@app.get("/stats")
async def combined_stats(response: Response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    stats = await toasties.get_live_stats()
    if stats == None:
        raise HTTPException(404, "Buttered Toast is not live")
    return stats

@app.get("/roster/{room}")
async def get_last_roster(room: int, response: Response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    roster = await toasties.get_last_roster(room)
    if roster is None:
        return []
    return roster

@app.post("/pantry/loadsheet")
async def load_sheet(ids: dict):
    # We shouldn't need this one
    pass

@app.post("/pantry/player")
async def add_player(player: Player, response: Response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    pid = await pantry.add_player(player)
    response.status_code = 201
    return {
        "id": pid
    }

@app.get("/pantry/players")
async def get_players(response: Response, played_since: int | None = None):
    response.headers['Access-Control-Allow-Origin'] = "*"
    players = await pantry.get_players(played_since)
    return players

@app.get("/pantry/toasts")
async def get_toasts(response: Response, content: Literal["Academic", "Trash"] | None = None):
    response.headers['Access-Control-Allow-Origin'] = "*"
    toasts = await pantry.get_toasts(content)
    return toasts

if __name__ == "__main__":
    uvicorn.run("main:app", log_level="info", reload=True, host="localhost", port=8000)