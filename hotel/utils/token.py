from functools import wraps
from typing import Any, Dict, Tuple

import jwt


def validate_token(token: str, JWT_SECRET) -> Tuple[bool, Dict[str, Any]]:  # noqa: F821
    """
    Validate JWT token and return decoded payload.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])  # noqa: F821
        return True, payload
    except jwt.InvalidTokenError:
        return False, {}


def require_valid_token(TOKEN):
    def decorator(f):
        """Decorator to check for valid JWT token"""

        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = kwargs.get("token")
            if not token:
                return {"message": "No token provided"}, 401

            is_valid, _ = validate_token(token, TOKEN)
            if not is_valid:
                return {"message": "Invalid token"}, 401

            return f(*args, **kwargs)

        return decorated_function

    return decorator
