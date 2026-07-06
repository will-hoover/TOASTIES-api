from fastapi import FastAPI, HTTPException
from contextvars import ContextVar

from fastapi.responses import Response
import uvicorn

from db.model import Scoresheet

toast: ContextVar[int | None] = ContextVar(None)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/toast")
async def current_toast(response: Response):
    # TODO: return current toast number - add toast to db if context is empty
    current = toast.get()
    if current is None:
        # Do DB stuff
        pass
    return { "toast": current }

@app.post("/end")
async def finish_toast(response: Response):
    # TODO: delete toast number from context
    pass

@app.post("/addroom")
async def addroom(response: Response):
    # TODO: increment room count for this toast
    pass

@app.get("/rooms")
async def rooms(response: Response):
    # TODO: get number of rooms for this toast
    pass

@app.get("/stats/{room_number}")
async def room_stats(room_number: int, response: Response):
    # TODO: get stats for the given room number
    pass

@app.get("combinedstats")
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