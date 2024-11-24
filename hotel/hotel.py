from pathlib import Path
from connexion import FlaskApp
from typing import Any, Dict, List, Optional, Tuple
import configparser
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from connexion.options import SwaggerUIOptions
from datetime import datetime
from utils.validation import validate_booking_dates
from utils.token import require_valid_token, validate_token
from utils.sql_function import (
    create_reservation,
    delete_reservation_by_id,
    fetch_room_detail_by_id,
    fetch_rooms,
    filter_by_availability,
    is_room_available,
)
from flask_cors import CORS

# Path configuration
root_path = Path(__file__).parent

# Load configurations from hotel.ini
config = configparser.ConfigParser()
config.read(root_path / "hotel.ini")

# Connexion App initialization
app = FlaskApp(__name__, specification_dir=str(root_path))
CORS(app.app, resources={r"/*": {"origins": "*"}})

options = SwaggerUIOptions(swagger_ui_path="/docs")

app.add_api("hotel.yaml", swagger_ui_options=options)

# Database Configuration
DATABASE_URI = config["DATABASE"]["URI"]
JWT_SECRET = config["SECURITY"]["JWT_SECRET"]

# Create SQLAlchemy engine and session
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
    Retrieve a list of rooms with optional filters.
    """
    try:
        with engine.connect() as connection:
            rooms = fetch_rooms(minsize, minprize, maxprice, beds, connection)

            if not rooms:
                return [], 204

            rooms_list = filter_by_availability(start_date, end_date, connection, rooms)

            return rooms_list, 200

    except Exception as e:
        return {"message": f"Database error: {str(e)}"}, 500


def get_room_details(uuid: str) -> Dict[str, Any]:
    """
    Retrieve detailed information for a specific room.
    """
    try:
        with engine.connect() as connection:
            result = fetch_room_detail_by_id(uuid, connection)

            if not result:
                return {"message": "Room not found"}, 404

            return dict(result._mapping), 200

    except Exception as e:
        return {"message": f"Database error: {str(e)}"}, 500


@require_valid_token(JWT_SECRET)
def book_room(uuid: str, token: str, body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Book a specific room.
    """
    try:
        # Business logic validation for dates
        is_valid, error = validate_booking_dates(body["start-date"], body["end-date"])
        if not is_valid:
            return {"message": error}, 400

        with engine.connect() as connection:
            if not is_room_available(
                uuid, body["start-date"], body["end-date"], connection
            ):
                return {"message": "Room isn't available for the selected dates"}, 409

            # Create reservation
            reservation = create_reservation(uuid, body, connection)

            if not reservation:
                return {"message": "Failed to create reservation"}, 500

            return dict(reservation[0]._mapping), 200

    except Exception as e:
        return {"message": f"Database error: {str(e)}"}, 500


@require_valid_token(JWT_SECRET)
def cancel_room_reservation(uuid: str, token: str) -> Dict[str, Any]:
    """
    Cancel a room reservation.
    """
    try:
        with engine.connect() as connection:
            # Verify reservation exists and belongs to user

            delete_reservation_by_id(uuid, token, connection)
            return {"message": "Reservation cancelled successfully"}, 200

    except Exception as e:
        return {"message": f"Database error: {str(e)}"}, 500


@require_valid_token(JWT_SECRET)
def update_room_reservation(
    uuid: str, token: str, body: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update a room reservation.
    """
    try:
        # Validate business logic for dates if provided
        if "start-date" in body or "end-date" in body:
            start_date = body.get("start-date")
            end_date = body.get("end-date")
            is_valid, error = validate_booking_dates(start_date, end_date)
            if not is_valid:
                return {"message": error}, 400

        with engine.connect() as connection:
            # Verify reservation exists and belongs to user
            is_valid, payload = validate_token(token)
            user_id = payload.get("user_id")

            # Check if reservation exists and is active
            reservation = connection.execute(
                text("""
                    SELECT room_id, start_date, end_date 
                    FROM reservations 
                    WHERE id = :uuid 
                    AND user_id = :user_id 
                    AND status = 'active'
                """),
                {"uuid": uuid, "user_id": user_id},
            ).fetchone()

            if not reservation:
                return {"message": "Reservation not found or not active"}, 404

            # If dates are being updated, check availability
            if "start-date" in body or "end-date" in body:
                new_start = body.get("start-date", reservation.start_date)
                new_end = body.get("end-date", reservation.end_date)

                if not is_room_available(
                    reservation.room_id,
                    new_start,
                    new_end,
                    connection,
                    exclude_reservation=uuid,
                ):
                    return {"message": "Room not available for new dates"}, 409

            # Update reservation
            update_fields = []
            params = {"uuid": uuid, "user_id": user_id}

            for field in ["start-date", "end-date", "guest-name", "guest-email"]:
                if field in body:
                    db_field = field.replace("-", "_")
                    update_fields.append(f"{db_field} = :{db_field}")
                    params[db_field] = body[field]

            if update_fields:
                query = f"""
                    UPDATE reservations 
                    SET {', '.join(update_fields)},
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = :uuid 
                    AND user_id = :user_id
                    RETURNING id, start_date, end_date, guest_name, guest_email
                """

                result = connection.execute(text(query), params).fetchone()
                return dict(result._mapping), 200

            return {"message": "No fields to update"}, 400

    except Exception as e:
        return {"message": f"Database error: {str(e)}"}, 500


def get_room_images(uuid: str) -> List[Dict[str, Any]]:
    """
    Retrieve images for a specific room.
    """
    try:
        with engine.connect() as connection:
            query = """
                SELECT url, description, created_at 
                FROM room_images 
                WHERE room_id = :uuid 
                ORDER BY created_at DESC
            """

            images = connection.execute(text(query), {"uuid": uuid}).fetchall()

            if not images:
                return [], 204

            return [dict(image._mapping) for image in images], 200

    except Exception as e:
        return {"message": f"Database error: {str(e)}"}, 500


def get_hotel_info() -> Dict[str, Any]:
    """
    Retrieve general information about the hotel.
    """
    try:
        return {
            "name": config["hotel_description"]["name"],
            "description": config["hotel_description"]["description"],
            "stars": int(config["hotel_description"]["stars"]),
            "address": config["hotel_description"].get("address", ""),
            "phone": config["hotel_description"].get("phone", ""),
            "email": config["hotel_description"].get("email", ""),
        }, 200
    except Exception as e:
        return {"message": f"Configuration error: {str(e)}"}, 500


def get_hotel_images() -> List[Dict[str, Any]]:
    """
    Retrieve a list of images of the hotel.
    """
    try:
        with engine.connect() as connection:
            query = """
                SELECT url, description, category, created_at 
                FROM hotel_images 
                ORDER BY category, created_at DESC
            """

            images = connection.execute(text(query)).fetchall()

            if not images:
                return [], 204

            return [dict(image._mapping) for image in images], 200

    except Exception as e:
        return {"message": f"Database error: {str(e)}"}, 500
