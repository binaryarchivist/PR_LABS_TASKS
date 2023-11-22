from functools import wraps

from flask import Flask, request, jsonify

import requests
import random


class Gateway:
    def __init__(self, cluster_nodes, leader_node):
        self.app = Flask(__name__)
        self.cluster_nodes = cluster_nodes
        self.leader_node = leader_node
        self.setup_routes()

    def handle_read(self, path):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                followers = [node for node in self.cluster_nodes if node != self.leader_node]
                if not followers:
                    response = requests.get(f'http://{self.leader_node.host}:{self.leader_node.port}/{path}')
                    return jsonify(response.json()), response.status_code
                node = random.choice(followers)
                try:
                    response = requests.get(f'http://{node.host}:{node.port}/{path}')
                    return jsonify(response.json()), response.status_code
                except requests.RequestException:
                    return jsonify({"error": "Failed to forward read request"}), 500

            return decorated_function

        return decorator

    def handle_write(self, method, path):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                try:
                    access_token = self.get_token()
                    body = request.get_json()
                    response = requests.request(method=method,
                                                url=f'http://{self.leader_node.host}:{self.leader_node.port}/{path}',
                                                headers={
                                                    'X-Access-Token': access_token,
                                                    'X-Origin-Role': 'leader',
                                                    'X-Delete-Password': request.headers.get('X-Delete-Password')
                                                },
                                                json=body)

                    # Notify followers of write operation
                    self.leader_node.replicate_to_followers(body)

                    return jsonify(response.json()), response.status_code
                except requests.RequestException as e:
                    return jsonify({"error": e}), 500

            return decorated_function

        return decorator

    def get_token(self):
        try:
            response = requests.get(f'http://{self.leader_node.host}:{self.leader_node.port}/token', headers={
                'X-Origin-Role': 'leader'
            })
            return response.json()['access_token']
        except requests.RequestException:
            return jsonify({"error": "Failed to process request"}), 500

    def setup_routes(self):
        @self.app.route('/ping', methods=['GET'])
        @self.handle_read('/ping')
        def ping():
            pass

        @self.app.route('/api/electro-scooters/<int:scooter_id>', methods=["GET"])
        @self.handle_read('/api/electro-scooters/<int:scooter_id>')
        def handle_read():
            pass

        @self.app.route('/api/electro-scooters', methods=['POST'])
        @self.handle_write('POST', '/api/electro-scooters')
        def create_scooter():
            pass

        @self.app.route('/api/electro-scooters/<int:scooter_id>', methods=['PUT'])
        @self.handle_write('PUT', '/api/electro-scooters/<int:scooter_id>')
        def update_scooter():
            pass

        @self.app.route('/api/electro-scooters/<int:scooter_id>', methods=['DELETE'])
        @self.handle_write('DELETE', '/api/electro-scooters/<int:scooter_id>')
        def delete_scooter():
            pass

    def run(self, host='127.0.0.1', port=9999):
        self.app.run(host=host, port=port)
