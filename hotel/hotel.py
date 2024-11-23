import array
import json
from logging import Logger
import os
from pathlib import Path
from uuid import UUID
from connexion import FlaskApp
from typing import Any, Dict, List, Optional
import configparser
import connexion
from flask import jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from connexion.options import SwaggerUIOptions


# Path configuration
root_path = Path(__file__).parent

# Load configurations from hotel.ini
config = configparser.ConfigParser()
config.read(root_path / "hotel.ini")

# Connexion App initialization
app = FlaskApp(__name__, specification_dir=str(root_path))
options = SwaggerUIOptions(swagger_ui_path="/docs")

app.add_api("hotel.yaml", swagger_ui_options=options)

# Database Configuration
DATABASE_URI = config["DATABASE"]["URI"]

# Create SQLAlchemy engine and session
engine = create_engine(DATABASE_URI, echo=True)  # echo=True logs SQL queries
SessionLocal = sessionmaker(bind=engine)


# Get all rooms
def get_rooms(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    minsize: Optional[int] = 0,
    minprize: Optional[float] = 0,
    maxprice: Optional[float] = 0b11111111,
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

    global engine

    with engine.connect() as connection:
        rooms = connection.execute(
            text(
                f"SELECT id,name,size,beds,price,description FROM rooms WHERE beds >= {beds} AND price >= {minprize} AND price <= {maxprice}"
            )
        ).fetchall()

        rooms_list = [dict(room._mapping) for room in rooms]

        return rooms_list, 200


# Get room detailed information
def get_room_details(uuid: str) -> Dict[str, Any]:
    """
    Retrieve detailed information for a specific room.

    Parameters:
        uuid (str): The unique identifier of the room.

    Returns:
        Dict[str, Any]: Detailed information about the room.
    """
    with engine.connect() as connection:
        rooms = connection.execute(
            text(
                f"SELECT id,name,size,beds,price,description FROM rooms WHERE id={uuid}"
            )
        ).fetchall()

        rooms_list = [dict(room._mapping) for room in rooms]

        return rooms_list, 200


# Book a room
def book_room(uuid: str, token: str, body) -> Dict[str, Any]:
    """
    Book a specific room.

    Parameters:
        uuid (str): The unique identifier of the room to be booked.

    Returns:
        Dict[str, Any]: Response data confirming the booking.
    """

    with engine.connect() as connection:
        reservation = connection.execute(
            text(
                "SELECT * FROM create_reservation('{}' ,'{}','{}')".format(
                    uuid, body["start-date"], body["end-date"]
                )
            )
        ).fetchall()

        connection.commit()

        return [dict(res._mapping) for res in reservation][0], 200

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


# Get room images
def get_room_images(uuid: str) -> List[Dict[str, Any]]:
    """
    Retrieve images for a specific room.

    Parameters:
        uuid (str): The unique identifier of the room.

    Returns:
        List[Dict[str, Any]]: A list of image data for the room.
    """
    return {}, 200


# Get hotel information
def get_hotel_info() -> Dict[str, Any]:
    global config

    """
    Retrieve general information about the hotel.

    Returns:
        Dict[str, Any]: Information about the hotel.
    """
    return {
        "name": config["hotel_description"]["name"],
        "description": config["hotel_description"]["description"],
        "stars": int(config["hotel_description"]["stars"]),
    }, 200


# Get hotel images
def get_hotel_images() -> List[Dict[str, Any]]:
    """
    Retrieve a list of images of the hotel.

    Returns:
        List[Dict[str, Any]]: A list of image data for the hotel.
    """
    return [], 200
