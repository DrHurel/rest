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
    hotel_book_room,
    hotel_get_hotel_info,
)
from flask_cors import CORS

from utils.tools import (
    cancel_reservation_at_hotel,
    fetch_room_details,
    fetch_rooms,
    fetch_services,
    get_hotel_domain,
    patch_reservation,
    save_reservations,
)

root_path = Path(__file__).parent

config = configparser.ConfigParser()
config.read(root_path / "agency.ini")

app = FlaskApp(__name__, specification_dir=str(root_path))
options = SwaggerUIOptions(swagger_ui_path="/docs")

CORS(app.app, resources={r"/*": {"origins": "*"}})


app.add_api("agency.yaml", swagger_ui_options=options)

DATABASE_URI = config["DATABASE"]["URI"]

engine = create_engine(DATABASE_URI, echo=True)  # echo=True logs SQL queries


def get_rooms(
    start_date: Optional[str] = None,
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

    if start_date is None:
        start_date = date.today()

    services = []
    try:
        with engine.connect() as connection:
            services = fetch_services(connection)
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
                details = fetch_room_details(domain, original_id, hotelClient)
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
                booking_result = book_hotel_room(token, body, original_id, hotelClient)

                with engine.connect() as connection:
                    save_reservations(body, domain, booking_result, connection)

                result = booking_result
                result["id"] = "{}-{}".format(domain, result.get("id"))
                return {}, 200

            except httpx.ConnectError as e:
                return {"error": f"Connection to hotel API failed: {str(e)}"}, 500
            except Exception as e:
                return {"error": f"An unexpected error occurred: {str(e)}"}, 500
    except ValueError as e:
        return {"error": str(e)}, 400


def book_hotel_room(token, body, original_id, hotelClient):
    booking_result = hotel_book_room.sync(
        uuid=original_id,
        token=token,
        body=HotelBookRoomBody(
            start_date=datetime.datetime.fromisoformat(body["start-date"]),
            end_date=datetime.datetime.fromisoformat(body["end-date"]),
        ),
        client=hotelClient,
    )

    return booking_result


def cancel_room_reservation(uuid: str, token: str) -> Dict[str, Any]:
    """
    Cancel a room reservation through the hotel's API.
    """
    try:
        domain, original_id = get_hotel_domain(uuid)

        with Client(f"http://{domain}/api/v1") as hotelClient:
            try:
                cancel_result = cancel_reservation_at_hotel(
                    engine, token, domain, original_id, hotelClient
                )

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
                result = patch_reservation(
                    engine, token, body, domain, original_id, hotelClient
                )
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
        agency_info = {
            "name": config["agency_description"]["name"],
            "description": config["agency_description"]["description"],
        }

        connected_hotels = []
        with engine.connect() as connection:
            hotels = connection.execute(text("SELECT domain FROM hotels")).fetchall()

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
