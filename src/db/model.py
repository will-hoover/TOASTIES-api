from pydantic import BaseModel, BeforeValidator, Field
from datetime import datetime
from typing import Annotated
from bson import ObjectId

# Custom type that converts BSON ObjectId to str automatically
PyObjectId = Annotated[str, BeforeValidator(lambda v: str(v) if isinstance(v, ObjectId) else v)]

class Player(BaseModel):
    id: PyObjectId = Field(alias="_id")
    alias: str
    firstName: str
    lastName: str
    lastToast: int

class Toast(BaseModel):
    id: PyObjectId = Field(None, alias="_id")
    number: int
    name: str # "Butt3r3d Toast", etc.
    date: datetime
    content: str # Trash or Academic
    rooms: int = 0
    live: bool = False

class Buzz(BaseModel):
    player: int
    points: int

class Scoresheet(BaseModel):
    id: PyObjectId = Field(alias="_id")
    toast: int
    room: int
    writer: int
    reader: int
    roster: list[int]
    questions: list[list[Buzz]]
    timestamp: datetime = datetime.now() # required for most recent roster call

def validated_player(player):
    return Player(**player).model_dump()

def validated_toast(toast):
    return Toast(**toast).model_dump()

def validated_scoresheet(scoresheet):
    return Scoresheet(scoresheet).model_dump()