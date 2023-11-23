import json
import socket


class Node:
    def __init__(self, host='127.0.0.1', port: int = 8000, buffer_size: int = 1024):
        self.host: str = host
        self.port: int = port
        self.role: str | None = None
        self.buffer_size: int = buffer_size

        self.udp_socket: socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.leader_port = None
        self.leader_host = None

        self.followers = []
        self.flask_app = {}
        self.initialize_socket()

    def initialize_socket(self) -> None:
        initialized: bool = False
        while not initialized:
            try:
                self.udp_socket.bind((self.host, self.port))
                initialized = True
            except OSError:
                # print(f"Port {self.port} is in use, trying next port.")
                self.port += 1

    def listen(self) -> None:
        while True:
            data, addr = self.udp_socket.recvfrom(self.buffer_size)

            message = json.loads(data.decode('utf-8'))
            print(f'Message received: {self.host}:{self.port}', message)

            if message['type'] == 'leader_credentials':
                self.leader_host = message['leader_host']
                self.leader_port = message['leader_port']

                self.send_message(self.leader_host, self.leader_port, {
                    'type': 'follower',
                    'follower_host': self.host,
                    'follower_port': self.port
                })
            elif message['type'] == 'follower':
                print(f"New follower: {message['follower_host']}:{message['follower_port']}")
                self.followers.append({
                    'host': message['follower_host'],
                    'port': message['follower_port']
                })
            elif message['type'] == 'replicate':
                print(f"Replicating data: {message['data']}")

    def send_message(self, host, port, msg) -> None:
        bytes_msg = json.dumps(msg).encode('utf-8')

        self.udp_socket.sendto(bytes_msg, (host, port))

    def replicate_to_followers(self, data):
        for follower in self.followers:
            self.send_message(follower['host'], follower['port'], {
                'type': 'replicate',
                'data': data
            })
