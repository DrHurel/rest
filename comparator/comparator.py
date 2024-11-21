from pathlib import Path
from typing import Any, Dict, List, Optional
from connexion import FlaskApp
import configparser
from connexion.options import SwaggerUIOptions

root_path = Path(__file__).parent

config = configparser.ConfigParser()
config.read(root_path / "comparator.ini")

app = FlaskApp(__name__)
options = SwaggerUIOptions(swagger_ui_path="/docs")
app.add_api(root_path / ".." / "api" / "comparator.yaml", swagger_ui_options=options)  # noqa: F821


def get_agency():
    return []
