from datetime import date
from pathlib import Path
from urllib import response
from connexion import FlaskApp
from typing import Any, Dict, List, Optional
import configparser
import httpx
from sqlalchemy import create_engine, text, values
from sqlalchemy.orm import sessionmaker
from connexion.options import SwaggerUIOptions
from generated.rest_hotel_api_client.client import Client
from generated.rest_hotel_api_client.api.default import hotel_get_rooms


# Path configuration
root_path = Path(__file__).parent

# Load configurations from hotel.ini
config = configparser.ConfigParser()
config.read(root_path / "agency.ini")

# Connexion App initialization
app = FlaskApp(__name__, specification_dir=str(root_path))
options = SwaggerUIOptions(swagger_ui_path="/docs")

app.add_api("agency.yaml", swagger_ui_options=options)

# Database Configuration
DATABASE_URI = config["DATABASE"]["URI"]

# Create SQLAlchemy engine and session
# engine = create_engine(DATABASE_URI, echo=True)  # echo=True logs SQL queries
# SessionLocal = sessionmaker(bind=engine)


# Get all rooms
def get_rooms(
    start_date: Optional[str] = date.today(),
    end_date: Optional[str] = None,
    minsize: Optional[int] = 0,
    minprize: Optional[float] = 0,
    maxprice: Optional[float] = 100000000,
    beds: Optional[int] = 1,
) -> List[Dict[str, Any]]:
    """
    Retrieve a list of rooms with optional filters.

    Parameters:
        start_date (str, optional): Start date for room availability filter.
        end_date (str, optional): End date for room availability filter.
        minsize (int, optional): Minimum room size filter.
        minprize (float, optional): Minimum price filter.
        maxprice (float, optional): Maximum price filter.
        beds (int, optional): Number of beds filter.

    Returns:
        List[Dict[str, Any]]: A list of rooms matching the criteria.
    """
    services = ["hotel-heritage:1234", "hotel-mountain:2345", "hotel-palm:3456"]
    res = []
    for service in services:
        with Client(f"http://{service}/api/v1") as hotelClient:
            try:
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
                    value["id"] = "{}-{}".format(service, value.get("id"))
                    res.append(value)
            except httpx.ConnectError as e:
                return {"error": f"Connection to hotel API failed : {str(e)}"}, 500
            except Exception as e:
                return {"error": f"An unexpected error occurred: {str(e)}"}, 500
    return res, 200


# Get room detailed information
def get_room_details(uuid: str) -> Dict[str, Any]:
    """
    Retrieve detailed information for a specific room.

    Parameters:
        uuid (str): The unique identifier of the room.

    Returns:
        Dict[str, Any]: Detailed information about the room.
    """

    return [], 200


# Book a room
def book_room(uuid: str, token: str, body) -> Dict[str, Any]:
    """
    Book a specific room.

    Parameters:
        uuid (str): The unique identifier of the room to be booked.

    Returns:
        Dict[str, Any]: Response data confirming the booking.
    """

    return {}, 200


def cancel_room_reservation(uuid: str, token: str) -> Dict[str, Any]:
    """
    Book a specific room.

    Parameters:
        uuid (str): The unique identifier of the room to be booked.

    Returns:
        Dict[str, Any]: Response data confirming the booking.
    """
    return 200


def update_room_reservation(uuid: str, token: str) -> Dict[str, Any]:
    """
    Book a specific room.

    Parameters:
        uuid (str): The unique identifier of the room to be booked.

    Returns:
        Dict[str, Any]: Response data confirming the booking.
    """
    return 200


# Get hotel information
def get_agency_info() -> Dict[str, Any]:
    global config

    """
    Retrieve general information about the hotel.

    Returns:
        Dict[str, Any]: Information about the hotel.
    """
    return {
        "name": config["agency_description"]["name"],
        "description": config["agency_description"]["description"],
    }, 200
