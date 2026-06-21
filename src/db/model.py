from typing import TypedDict

class Player(TypedDict):
    _id: int
    FirstName: str
    LastName: str

class Toast(TypedDict):
    Number: int
    Name: str # "Butt3r3d Toast", etc.
    Date: str # I don't feel like dealing with the datetime data type

class Buzz(TypedDict):
    Player: int
    Points: int

class Scoresheet(TypedDict):
    Toast: int
    Room: int
    Writer: int
    Reader: int
    Roster: list[int]
    Questions: list[list[Buzz]]