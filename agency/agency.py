from pathlib import Path
from connexion import FlaskApp
import configparser
from connexion.options import SwaggerUIOptions


root_path = Path(__file__).parent

config = configparser.ConfigParser()
config.read(root_path / "agency.ini")

app = FlaskApp(__name__)
options = SwaggerUIOptions(swagger_ui_path="/docs")

app = FlaskApp(__name__)
app.add_api(root_path / "../api/agency.yaml")  # noqa: F821
