from sqlalchemy import Connection, text

from utils.token import validate_token


def is_room_available(uuid, start_date, end_date, connection: Connection):
    try:
        return connection.execute(
            text(
                "SELECT is_room_available('{}', '{}','{}')".format(
                    uuid, start_date, end_date
                )
            )
        ).scalar()
    except Exception:
        return False


def create_reservation(uuid, body, connection: Connection):
    res = connection.execute(
        text(
            "SELECT * FROM create_reservation('{}' ,'{}','{}')".format(
                uuid, body["start-date"], body["end-date"]
            )
        )
    ).fetchone()
    connection.commit()

    return res[0]


def filter_by_availability(start_date, end_date, connection, rooms):
    rooms_list = [dict(room._mapping) for room in rooms]

    # Filter by availability if dates provided
    if start_date and end_date:
        rooms_list = [
            room
            for room in rooms_list
            if is_room_available(room["id"], start_date, end_date, connection)
        ]

    return rooms_list


def fetch_rooms(minsize, minprize, maxprice, beds, connection):
    query = """
                SELECT id, name, size, beds, price, description 
                FROM rooms 
                WHERE beds >= :beds 
                AND price >= :minprize 
                AND price <= :maxprice 
                AND size >= :minsize
            """

    params = {
        "beds": beds,
        "minprize": minprize,
        "maxprice": maxprice,
        "minsize": minsize,
    }

    rooms = connection.execute(text(query), params).fetchall()
    return rooms


def fetch_room_detail_by_id(uuid, connection):
    query = """
                SELECT r.id, r.name, r.size, r.beds, r.price, r.description,
                       array_agg(DISTINCT a.name) as amenities,
                       array_agg(DISTINCT i.url) as images
                FROM rooms r
                LEFT JOIN room_amenities ra ON r.id = ra.room_id
                LEFT JOIN amenities a ON ra.amenity_id = a.id
                LEFT JOIN room_images i ON r.id = i.room_id
                WHERE r.id = :uuid
                GROUP BY r.id, r.name, r.size, r.beds, r.price, r.description
            """

    result = connection.execute(text(query), {"uuid": uuid}).fetchone()
    return result


def delete_reservation_by_id(uuid, token, connection):
    _, payload = validate_token(token)
    user_id = payload.get("user_id")
    query = """
                DELETE reservations 
                WHERE id = :uuid 
            """

    connection.execute(text(query), {"uuid": uuid, "user_id": user_id})
