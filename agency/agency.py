from datetime import date
import datetime
from pathlib import Path
from connexion import FlaskApp
from typing import Any, Dict, List, Optional
import configparser
import httpx
from sqlalchemy import create_engine, text
from connexion.options import SwaggerUIOptions
from generated.rest_hotel_api_client.models.hotel_book_room_body import (
    HotelBookRoomBody,
)
from generated.rest_hotel_api_client.client import Client
from generated.rest_hotel_api_client.api.default import (
    hotel_get_room_details,
    hotel_book_room,
    hotel_cancel_room_reservation,
    hotel_update_room_reservation,
    hotel_get_hotel_info,
)
from flask_cors import CORS

from utils.tools import fetch_rooms, get_hotel_domain

# Path configuration
root_path = Path(__file__).parent

# Load configurations from hotel.ini
config = configparser.ConfigParser()
config.read(root_path / "agency.ini")


# Connexion App initialization
app = FlaskApp(__name__, specification_dir=str(root_path))
options = SwaggerUIOptions(swagger_ui_path="/docs")

CORS(app.app, resources={r"/*": {"origins": "*"}})


app.add_api("agency.yaml", swagger_ui_options=options)

# Database Configuration
DATABASE_URI = config["DATABASE"]["URI"]

engine = create_engine(DATABASE_URI, echo=True)  # echo=True logs SQL queries


def get_rooms(
    start_date: Optional[str] = date.today(),
    end_date: Optional[str] = None,
    minsize: Optional[int] = 0,
    minprize: Optional[float] = 0,
    maxprice: Optional[float] = 100000000,
    beds: Optional[int] = 1,
) -> List[Dict[str, Any]]:
    """
    Retrieve a list of rooms from all connected hotels with optional filters.
    """
    global engine
    services = []
    try:
        with engine.connect() as connection:
            hotels = connection.execute(
                text("SELECT domain,rooms_margins FROM hotels")
            ).fetchall()
            services = [hotel._mapping for hotel in hotels]
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}, 500

    res = []
    try:
        fetch_rooms(
            start_date, end_date, minsize, minprize, maxprice, beds, services, res
        )
    except httpx.ConnectError as e:
        return {"error": f"Connection to hotel API failed: {str(e)}"}, 500
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}, 500
    return res, 200


def get_room_details(uuid: str) -> Dict[str, Any]:
    """
    Retrieve detailed information for a specific room.
    """
    try:
        domain, original_id = get_hotel_domain(uuid)

        with Client(f"http://{domain}/api/v1") as hotelClient:
            try:
                room_details = hotel_get_room_details.sync(
                    uuid=original_id, client=hotelClient
                )

                details = room_details.to_dict()
                details["id"] = f"{domain}-{details.get('id')}"
                return details, 200

            except httpx.ConnectError as e:
                return {"error": f"Connection to hotel API failed: {str(e)}"}, 500
            except Exception as e:
                return {"error": f"An unexpected error occurred: {str(e)}"}, 500
    except ValueError as e:
        return {"error": str(e)}, 400


def book_room(uuid: str, token: str, body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Book a specific room through the hotel's API.
    """
    try:
        domain, original_id = get_hotel_domain(uuid)

        with Client(f"http://{domain}/api/v1") as hotelClient:
            try:
                # Forward the booking request to the hotel
                booking_result = hotel_book_room.sync(
                    uuid=original_id,
                    token=token,
                    body=HotelBookRoomBody(
                        start_date=datetime.datetime.fromisoformat(body["start-date"]),
                        end_date=datetime.datetime.fromisoformat(body["end-date"]),
                    ),
                    client=hotelClient,
                )

                print(booking_result)

                # Store the booking in our database
                with engine.connect() as connection:
                    query = """INSERT INTO reservations (reservation_id, hotel_id, customer_name, customer_email, check_in_date, check_out_date, total_price, reservation_status) VALUES (:reservation_id, :hotel_id, :customer_name, :customer_email, :check_in_date, :check_out_date, :total_price, :reservation_status) RETURNING reservation_id"""

                    params = {
                        "reservation_id": booking_result.id,
                        "hotel_id": domain,  # Assuming "domain" corresponds to the hotel ID
                        "customer_name": body.get(
                            "guest-name"
                        ),  # guest_name -> customer_name
                        "customer_email": body.get(
                            "guest-email"
                        ),  # guest_email -> customer_email
                        "check_in_date": body.get(
                            "start-date"
                        ),  # start_date -> check_in_date
                        "check_out_date": body.get(
                            "end-date"
                        ),  # end_date -> check_out_date
                        "total_price": 500,  # Replace with your actual logic to calculate the price
                        "reservation_status": "Pending",  # Default reservation status
                    }

                    connection.execute(text(query), params)
                    connection.commit()
                    print(token)
                # result = booking_result
                # result["id"] = "{}-{}".format(domain, result.get("id"))
                return {}, 200

            except httpx.ConnectError as e:
                return {"error": f"Connection to hotel API failed: {str(e)}"}, 500
            except Exception as e:
                return {"error": f"An unexpected error occurred: {str(e)}"}, 500
    except ValueError as e:
        return {"error": str(e)}, 400


def cancel_room_reservation(uuid: str, token: str) -> Dict[str, Any]:
    """
    Cancel a room reservation through the hotel's API.
    """
    try:
        domain, original_id = get_hotel_domain(uuid)

        with Client(f"http://{domain}/api/v1") as hotelClient:
            try:
                # Forward the cancellation request to the hotel
                cancel_result = hotel_cancel_room_reservation.sync(
                    uuid=original_id, token=token, client=hotelClient
                )

                # Update our database
                with engine.connect() as connection:
                    query = """
                        UPDATE bookings 
                        SET status = 'cancelled', 
                            cancelled_at = CURRENT_TIMESTAMP 
                        WHERE hotel_domain = :domain 
                        AND booking_id = :booking_id
                    """
                    connection.execute(
                        text(query), {"domain": domain, "booking_id": original_id}
                    )
                    connection.commit()

                return cancel_result.to_dict(), 200

            except httpx.ConnectError as e:
                return {"error": f"Connection to hotel API failed: {str(e)}"}, 500
            except Exception as e:
                return {"error": f"An unexpected error occurred: {str(e)}"}, 500
    except ValueError as e:
        return {"error": str(e)}, 400


def update_room_reservation(
    uuid: str, token: str, body: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update a room reservation through the hotel's API.
    """
    try:
        domain, original_id = get_hotel_domain(uuid)

        with Client(f"http://{domain}/api/v1") as hotelClient:
            try:
                # Forward the update request to the hotel
                update_result = hotel_update_room_reservation.sync(
                    uuid=original_id, token=token, body=body, client=hotelClient
                )

                # Update our database
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
                            UPDATE bookings 
                            SET {', '.join(update_fields)},
                                updated_at = CURRENT_TIMESTAMP
                            WHERE hotel_domain = :domain 
                            AND booking_id = :booking_id
                        """
                        connection.execute(text(query), params)
                        connection.commit()

                result = update_result.to_dict()
                result["id"] = f"{domain}-{result.get('id')}"
                return result, 200

            except httpx.ConnectError as e:
                return {"error": f"Connection to hotel API failed: {str(e)}"}, 500
            except Exception as e:
                return {"error": f"An unexpected error occurred: {str(e)}"}, 500
    except ValueError as e:
        return {"error": str(e)}, 400


def get_agency_info() -> Dict[str, Any]:
    """
    Retrieve general information about the agency.
    """
    try:
        # Get agency information from config
        agency_info = {
            "name": config["agency_description"]["name"],
            "description": config["agency_description"]["description"],
        }

        # Get list of connected hotels
        connected_hotels = []
        with engine.connect() as connection:
            hotels = connection.execute(text("SELECT domain FROM hotels")).fetchall()

            # Get information for each connected hotel
            for hotel in hotels:
                domain = hotel._mapping["domain"]
                with Client(f"http://{domain}/api/v1") as hotelClient:
                    try:
                        hotel_info = hotel_get_hotel_info.sync(client=hotelClient)
                        connected_hotels.append(
                            {"domain": domain, **hotel_info.to_dict()}
                        )
                    except (httpx.ConnectError, Exception):
                        # Skip hotels that are not responding
                        continue

        agency_info["connected_hotels"] = connected_hotels
        return agency_info, 200

    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}, 500
