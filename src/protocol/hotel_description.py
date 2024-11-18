from dataclasses import dataclass


@dataclass
class HotelDescription:
    country: str
    city: str
    street: str
    number: int
    gps: str
    stars: int
    locality: str
