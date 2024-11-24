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
        with Client("http://{}/api/v1".format(service["domain"])) as hotelClient:
            rooms = []
            if end_date is not None:
                rooms = hotel_get_rooms.sync(
                    start_date=start_date,
                    end_date=end_date,
                    minsize=minsize,
                    minprize=minprize,
                    maxprice=maxprice,
                    beds=beds,
                    client=hotelClient,
                )
            else:
                rooms = hotel_get_rooms.sync(
                    start_date=start_date,
                    minsize=minsize,
                    minprize=minprize,
                    maxprice=maxprice,
                    beds=beds,
                    client=hotelClient,
                )
            for room in rooms:
                value = room.to_dict()
                value["price"] = int(value["price"]) + int(value["price"]) * float(
                    service["rooms_margins"]
                )
                value["id"] = "{}|{}".format(service["domain"], value.get("id"))
                res.append(value)
