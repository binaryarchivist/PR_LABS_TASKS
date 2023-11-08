import socket
import threading
import json

import pika

CHUNK_SIZE = 4096


class Server:
    def __init__(self, host, port):
        self.clients = []
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server is listening on {self.host}:{self.port}")

    @staticmethod
    def format_message(msg_type, payload):
        return json.dumps({"type": msg_type, "payload": payload})

    def broadcast(self, message):
        for client in self.clients:
            try:
                client.send(message.encode('utf-8'))
            except:
                self.clients.remove(client)

    def message_cb(self, ch, method, properties, body):
        message_data = eval(body.decode())
        broadcast_message = {}
        # print(f" [x] Received {message_data}")

        if message_data["type"] == "connect":
            client_name = message_data["payload"]["name"]
            broadcast_message = self.format_message("notification",
                                               {"message": f"{client_name} has joined the room."})

        elif message_data["type"] == "message":
            client_name = message_data["payload"]["sender"]
            client_room = message_data["payload"]["room"]

            broadcast_message = self.format_message("message", {
                "sender": client_name,
                "room": client_room,
                "text": message_data["payload"]["text"]
            })

        self.broadcast(broadcast_message)

    def handle_client(self, client_socket, client_address):
        print(f"Accepted connection from {client_address}")
        host, port = client_address
        client_queue = "".join([str(host), ':', str(port)])

        connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
        channel = connection.channel()
        channel.queue_declare(queue=client_queue)
        channel.basic_consume(queue=client_queue, on_message_callback=self.message_cb, auto_ack=True)
        channel.start_consuming()

        self.clients.remove(client_socket)
        client_socket.close()

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.clients.append(client_socket)
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()


if __name__ == "__main__":
    server = Server('127.0.0.1', 12345)
    server.start()
