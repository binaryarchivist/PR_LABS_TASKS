# LAB6.py
from flask import Flask

from models.database import db
from init_db import init_database

from flask_swagger_ui import get_swaggerui_blueprint

from dotenv import load_dotenv
import os

SWAGGER_URL = "/docs"
API_URL = "/static/docs.json"


def create_app():
    load_dotenv()
    app = Flask(__name__)

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


if __name__ == "__main__":
    app = create_app()
    app = init_database(app)

    import routes

    app.run()
