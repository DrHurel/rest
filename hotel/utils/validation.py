from datetime import datetime
from typing import Tuple


def validate_booking_dates(
    start_date: datetime, end_date: datetime
) -> Tuple[bool, str]:
    """
    Validate booking date logic.
    """
    print("ézdvaba")
    if start_date >= end_date:
        return False, "End date must be after start date"

    if start_date < datetime.now():
        return False, "Start date cannot be in the past"

    print("testagazd")
    return True, ""
