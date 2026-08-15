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
    player: str
    points: int

class Scoresheet(BaseModel):
    # id: PyObjectId = Field(None, alias="_id")
    toast: str
    room: int
    writer: str
    reader: str | None = None
    roster: list[str]
    questions: list[list[Buzz]]
    timestamp: datetime = datetime.now() # required for most recent roster call

class Statline(BaseModel):
    name: str
    played: int = 0
    powers: int = 0
    gets: int = 0
    negs: int = 0
    written: int = 0
    read: int = 0

    def points(self) -> int:
        return 15*self.powers + 10*self.gets + -5*self.negs + min(10*self.written, 200) + min(5*self.read, 100)
    
    def ppg(self) -> float:
        if self.played == 0:
            return 0
        else:
            return (15*self.powers + 10*self.gets + -5*self.negs) / (self.played / 20)
        
    def add_buzz(self, value: int):
        if value == 10:
            self.gets += 1
        elif value == 15:
            self.powers += 1
        elif value == -5:
            self.negs += 1

    def add_stats(self, stats: Statline):
        self.played += stats.played
        self.powers += stats.powers
        self.gets += stats.gets
        self.negs += stats.negs
        self.read += stats.read
        self.written += stats.written

    def to_data_row(self):
        return [self.name, self.played, self.powers, self.gets, self.negs, self.written, self.read, self.ppg(), self.points()]

def validated_player(player):
    return Player(**player).model_dump()

def validated_toast(toast):
    return Toast(**toast).model_dump()

def validated_scoresheet(scoresheet):
    return Scoresheet(scoresheet).model_dump()