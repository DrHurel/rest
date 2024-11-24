from sqlalchemy import text
from generated.rest_hotel_api_client.client import Client
from generated.rest_hotel_api_client.api.default import (
    hotel_get_rooms,
    hotel_update_room_reservation,
    hotel_cancel_room_reservation,
    hotel_get_room_details,
)


def get_hotel_domain(room_id: str) -> tuple[str, str]:
    """Extract hotel domain and original room ID from composite ID"""
    try:
        [domain, original_id] = room_id.split("_")
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
                value["id"] = "{}_{}".format(service["domain"], value.get("id"))
                res.append(value)


def fetch_services(connection):
    hotels = connection.execute(
        text("SELECT domain,rooms_margins FROM hotels")
    ).fetchall()
    services = [hotel._mapping for hotel in hotels]
    return services


def patch_reservation(engine, token, body, domain, original_id, hotelClient):
    update_result = hotel_update_room_reservation.sync(
        uuid=original_id, token=token, body=body, client=hotelClient
    )

    with engine.connect() as connection:
        update_fields = []
        params = {"domain": domain, "booking_id": original_id}

        for field in [
            "start-date",
            "end-date",
            "guest-name",
            "guest-email",
        ]:
            if field in body:
                db_field = field.replace("-", "_")
                update_fields.append(f"{db_field} = :{db_field}")
                params[db_field] = body[field]

        if update_fields:
            query = f"""
                            UPDATE reservations 
                            SET {', '.join(update_fields)},
                                updated_at = CURRENT_TIMESTAMP
                            WHERE hotel_domain = :domain 
                            AND booking_id = :booking_id
                        """
            connection.execute(text(query), params)
            connection.commit()

    result = update_result
    result["id"] = f"{domain}-{result.get('id')}"
    return result


def cancel_reservation_at_hotel(engine, token, domain, original_id, hotelClient):
    cancel_result = hotel_cancel_room_reservation.sync(
        uuid=original_id, token=token, client=hotelClient
    )
    with engine.connect() as connection:
        query = """
                        UPDATE reservations 
                        SET status = 'cancelled', 
                            cancelled_at = CURRENT_TIMESTAMP 
                        WHERE hotel_domain = :domain 
                        AND booking_id = :booking_id
                    """
        connection.execute(text(query), {"domain": domain, "booking_id": original_id})
        connection.commit()
    return cancel_result


def save_reservations(body, domain, booking_result, connection):
    query = """INSERT INTO reservations (reservation_id, hotel_id, customer_name, customer_email, check_in_date, check_out_date, total_price, reservation_status) VALUES (:reservation_id, :hotel_id, :customer_name, :customer_email, :check_in_date, :check_out_date, :total_price, :reservation_status) RETURNING reservation_id"""

    params = {
        "reservation_id": booking_result.id,
        "hotel_id": connection.execute(
            text(f"""SELECT hotel_id from hotels WHERE domain = '{domain}'""")
        ).scalar(),  # Assuming "domain" corresponds to the hotel ID
        "customer_name": body.get("guest-name", "test"),  # guest_name -> customer_name
        "customer_email": body.get(
            "guest-email", "test"
        ),  # guest_email -> customer_email
        "check_in_date": body.get("start-date"),  # start_date -> check_in_date
        "check_out_date": body.get("end-date"),  # end_date -> check_out_date
        "total_price": 500,  # Replace with your actual logic to calculate the price
        "reservation_status": "Pending",  # Default reservation status
    }

    connection.execute(text(query), params)
    connection.commit()


def fetch_room_details(domain, original_id, hotelClient):
    room_details = hotel_get_room_details.sync(uuid=original_id, client=hotelClient)

    details = room_details.to_dict()
    details["id"] = f"{domain}-{details.get('id')}"
    return details
