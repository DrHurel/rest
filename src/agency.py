from pathlib import Path
from connexion import FlaskApp
import configparser


app = FlaskApp(__name__)
app.add_api(Path(__file__).parent / "../api/agency.yaml")  # noqa: F821


def post_greeting(name: str):
    return f"Hello {name}", 200
