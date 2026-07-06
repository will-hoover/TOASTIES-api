from pydantic import BaseModel

class Player(BaseModel):
    _id: int
    first_name: str
    last_name: str
    last_toast: int


class Toast(BaseModel):
    number: int
    name: str # "Butt3r3d Toast", etc.
    date: str # I don't feel like dealing with the datetime data type
    trash_day: bool

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