from flask import Flask

from .database.database import db
from .routes.routes import register_routes
from flask_swagger_ui import get_swaggerui_blueprint

from dotenv import load_dotenv
import os

SWAGGER_URL = "/docs"
API_URL = "/static/docs.json"


def initialize_flask(host: str, port: int) -> Flask:
    load_dotenv()
    app = Flask(f'{host}:{port}')

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'Access API'
        }
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    postgres_db = os.getenv("POSTGRES_DB")

    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f'postgresql://{postgres_user}:{postgres_password}@127.0.0.1:5432/{postgres_db}'

    db.init_app(app)
    return app


def startup_server(host: str, port: int) -> Flask:
    flask_app = initialize_flask(host, port)
    register_routes(flask_app)
    flask_app.run(host, port)
    return flask_app

