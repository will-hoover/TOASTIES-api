from pydantic import BaseModel

class Player(BaseModel):
    _id: int
    FirstName: str
    LastName: str

class Toast(BaseModel):
    Number: int
    Name: str # "Butt3r3d Toast", etc.
    Date: str # I don't feel like dealing with the datetime data type
    TrashDay: bool

class Buzz(BaseModel):
    Player: int
    Points: int

class Scoresheet(BaseModel):
    Toast: int
    Room: int
    Writer: int
    Reader: int
    Roster: list[int]
    Questions: list[list[Buzz]]

def validated_player(player):
    return Player(**player).model_dump()

def validated_toast(toast):
    return Toast(**toast).model_dump()

def validated_scoresheet(scoresheet):
    return Scoresheet(scoresheet).model_dump()