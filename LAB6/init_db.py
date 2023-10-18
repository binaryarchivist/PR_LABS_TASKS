# init_db.py
from models.database import db
from models.electro_scooter import ElectroScooter


def init_database(app):
    with app.app_context():
        # Create the database tables
        db.create_all()

        # Initialize the database with sample data (optional)
        sample_scooter_1 = ElectroScooter(name="Scooter 1", battery_level=90.5)
        sample_scooter_2 = ElectroScooter(name="Scooter 2", battery_level=80.0)
        db.session.add(sample_scooter_1)
        db.session.add(sample_scooter_2)
        db.session.commit()

    return app


if __name__ == "__main__":
    init_database()
