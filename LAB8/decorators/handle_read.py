from functools import wraps
from flask import jsonify
import requests
import random


def handle_read(cluster_nodes):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            node = random.choice(cluster_nodes)
            try:
                response = requests.get(f'http://{node[0]}:{node[1]}/ping')
                return jsonify(response.json()), response.status_code
            except requests.RequestException:
                return jsonify({"error": "Failed to forward read request"}), 500

        return decorated_function

    return decorator
