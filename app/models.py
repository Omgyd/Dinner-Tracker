from dataclasses import dataclass


@dataclass
class User:
    _id: str
    email: str
    password: str
