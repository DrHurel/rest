from dataclasses import dataclass


@dataclass
class Room:
    uuid: str
    beds: int
    size: int
    price: float
