from pydantic import BaseModel
import datetime

class Player(BaseModel):
    _id: int
    firstName: str
    lastName: str
    lastToast: int

class Toast(BaseModel):
    _id: int
    number: int
    name: str # "Butt3r3d Toast", etc.
    date: datetime
    trashDay: bool

class Buzz(BaseModel):
    player: int
    points: int

class Scoresheet(BaseModel):
    toast: int
    room: int
    writer: int
    reader: int
    roster: list[int]
    questions: list[list[Buzz]]

def validated_player(player):
    return Player(**player).model_dump()

def validated_toast(toast):
    return Toast(**toast).model_dump()

def validated_scoresheet(scoresheet):
    return Scoresheet(scoresheet).model_dump()