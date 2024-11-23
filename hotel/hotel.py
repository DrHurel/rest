import array
import json
from logging import Logger
from pathlib import Path
from connexion import FlaskApp
from typing import Any, Dict, List, Optional
import configparser
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


# Function to test the connection
def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print(f"Database connected: {result.scalar()}")
    except Exception as e:
        print(f"Database connection failed: {e}")


# Test the database connection
test_connection()


# Get all rooms
def get_rooms(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    minsize: Optional[int] = None,
    minprize: Optional[float] = None,
    maxprice: Optional[float] = None,
    beds: Optional[int] = None,
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
        rooms = connection.execute(text("SELECT * FROM rooms")).fetchall()

        rooms_list = [[data for data in room.tuple()] for room in rooms]

        return jsonify(rooms_list), 200
    return 501


# Get room detailed information
def get_room_details(uuid: str) -> Dict[str, Any]:
    """
    Retrieve detailed information for a specific room.

    Parameters:
        uuid (str): The unique identifier of the room.

    Returns:
        Dict[str, Any]: Detailed information about the room.
    """
    return {}, 200


# Book a room
def book_room(uuid: str, token: str) -> Dict[str, Any]:
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
