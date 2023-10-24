from dataclasses import dataclass


@dataclass
class User:
    _id: str
    email: str
    password: str
    first_name: str
    last_name: str
    group_number: str


@dataclass
class Dish:
    _id: str
    name: str
    ingredients: str
    time: str

@dataclass
class Grocery:
    _id: str
    item:list

