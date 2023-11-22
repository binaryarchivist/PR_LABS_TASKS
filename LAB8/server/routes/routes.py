from flask import jsonify, request, Flask

import secrets
from datetime import datetime, timedelta

from ..database.database import db
from ..models.electro_scooter import ElectroScooter
from ..decorators.security import secured
from ..models.token import Token


def register_routes(app: Flask) -> None:
    @app.route('/ping', methods=['GET'])
    # @secured
    def ping():
        return jsonify({"message": "Pinged !"})

    @app.route('/token', methods=['GET'])
    def get_access_token():
        role: str = request.headers.get('X-Origin-Role')

        if role != 'leader':
            return jsonify({"message": "Resource can be accessed just by leaders"}), 403

        new_token = secrets.token_urlsafe(16)
        expiration_time = datetime.now() + timedelta(hours=1)

        token = Token(token=new_token, expiration_time=expiration_time)
        db.session.add(token)
        db.session.commit()

        return jsonify({
            "access_token": new_token
        })

    @app.route('/api/electro-scooters', methods=['POST'])
    @secured
    def create_electro_scooter():
        try:
            data = request.get_json()

            name = data['name']
            battery_level = data['battery_level']

            electro_scooter = ElectroScooter(name=name, battery_level=battery_level)

            db.session.add(electro_scooter)
            db.session.commit()
            return jsonify({"message": "Electro Scooter created successfully"}), 201

        except KeyError:
            return jsonify({"error": "Invalid request data"}), 400

    @app.route('/api/electro-scooters/<int:scooter_id>', methods=["GET"])
    @secured
    def get_electro_scooter_by_id(scooter_id):
        scooter = ElectroScooter.query.get(scooter_id)
        if scooter is not None:
            return jsonify({
                "id": scooter.id,
                "name": scooter.name,
                "battery_level": scooter.battery_level
            }), 200
        else:
            return jsonify({"error": "Electro Scooter not found"}), 404

    @app.route('/api/electro-scooters/<int:scooter_id>', methods=['PUT'])
    @secured
    def update_electro_scooter(scooter_id):
        try:
            scooter = ElectroScooter.query.get(scooter_id)
            if scooter is not None:
                data = request.get_json()

                scooter.name = data.get('name', scooter.name)
                scooter.battery_level = data.get('battery_level', scooter.battery_level)

                db.session.commit()
                return jsonify({"message": "Electro Scooter updated successfully"}), 200
            else:
                return jsonify({"error": "Electro Scooter not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/electro-scooters/<int:scooter_id>', methods=['DELETE'])
    @secured
    def delete_electro_scooter(scooter_id):
        try:
            scooter = ElectroScooter.query.get(scooter_id)
            if scooter is not None:
                password = request.headers.get('X-Delete-Password')
                if password == 'your_secret_password':
                    db.session.delete(scooter)
                    db.session.commit()
                    return jsonify({"message": "Electro Scooter deleted successfully"}), 200
                else:
                    return jsonify({"error": "Incorrect password"}), 401
            else:
                return jsonify({"error": "Electro Scooter not found"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500
