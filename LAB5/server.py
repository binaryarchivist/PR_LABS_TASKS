import socket
import threading
import json


class Chat:
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

    def handle_client(self, client_socket, client_address):
        print(f"Accepted connection from {client_address}")
        client_name = ""
        client_room = ""

        while True:
            try:
                message_json = client_socket.recv(1024).decode('utf-8')
                if not message_json:
                    break
                message_data = json.loads(message_json)
                if message_data["type"] == "connect":
                    client_name = message_data["payload"]["name"]
                    client_room = message_data["payload"]["room"]
                    ack_message = self.format_message("connect_ack", {"message": "Connected to the room."})
                    client_socket.send(ack_message.encode('utf-8'))
                    notification = self.format_message("notification",
                                                       {"message": f"{client_name} has joined the room."})
                    self.broadcast(notification)

                elif message_data["type"] == "message":
                    broadcast_message = self.format_message("message", {
                        "sender": client_name,
                        "room": client_room,
                        "text": message_data["payload"]["text"]
                    })
                    self.broadcast(broadcast_message)

            except json.JSONDecodeError:
                print(f"Received invalid JSON data from {client_address}. Disconnecting client...")
                break

        self.clients.remove(client_socket)
        client_socket.close()

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.clients.append(client_socket)
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()


if __name__ == "__main__":
    server = Chat('127.0.0.1', 12345)
    server.start()
