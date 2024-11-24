from generated.rest_hotel_api_client.client import Client
from generated.rest_hotel_api_client.api.default import hotel_get_rooms


def get_hotel_domain(room_id: str) -> tuple[str, str]:
    """Extract hotel domain and original room ID from composite ID"""
    try:
        domain, original_id = room_id.split("|", 1)
        return domain, original_id
    except ValueError:
        raise ValueError("Invalid room ID format")


def fetch_rooms(start_date, end_date, minsize, minprize, maxprice, beds, services, res):
    for service in services:
        with Client(f"http://{service}/api/v1") as hotelClient:
            rooms = hotel_get_rooms.sync(
                start_date=start_date,
                end_date=end_date,
                minsize=minsize,
                minprize=minprize,
                maxprice=maxprice,
                beds=beds,
                client=hotelClient,
            )
            for room in rooms:
                value = room.to_dict()
                value["id"] = f"{service}|{value.get('id')}"
                res.append(value)
