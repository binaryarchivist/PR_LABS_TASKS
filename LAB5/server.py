import base64
import os
import socket
import threading
import json

from time import sleep

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

    def handle_client(self, client_socket, client_address):
        print(f"Accepted connection from {client_address}")
        client_name = ""
        client_room = ""

        while True:
            try:
                message_json = client_socket.recv(8192).decode('utf-8')
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

                elif message_data["type"] == "upload":
                    binary = message_data["payload"]["binary"]
                    file_name = message_data["payload"]["file_name"]
                    is_completed = message_data["payload"]["is_completed"]
                    with open(f'./media-server/{file_name}', 'ab') as file:
                        decoded_chunk = base64.b64decode(binary)
                        file.write(decoded_chunk)
                        file.flush()
                        file.close()

                    if is_completed:
                        broadcast_message = self.format_message("message", {
                            "sender": client_name,
                            "room": client_room,
                            "text": f'User {client_name} uploaded the {file_name} file'
                        })
                        self.broadcast(broadcast_message)

                elif message_data["type"] == "download":
                    file_name = message_data["payload"]["file_name"]
                    if not os.path.isfile(f'./media-server/{file_name}'):
                        broadcast_message = self.format_message("message", {
                            "sender": client_name,
                            "room": client_room,
                            "text": f'The {file_name} doesn\'t exist'
                        })
                        client_socket.send(broadcast_message.encode('utf-8'))

                    with open(f'./media-server/{file_name}', "rb") as file:
                        chunk = file.read(CHUNK_SIZE)
                        while chunk:
                            base64_chunk = base64.b64encode(chunk).decode('utf-8')
                            broadcast_message = self.format_message("download", {
                                "sender": client_name,
                                "room": client_room,
                                "binary": base64_chunk,
                                "file_name": file_name
                            })
                            client_socket.send(broadcast_message.encode('utf-8'))
                            sleep(1)
                            chunk = file.read(CHUNK_SIZE)

                        broadcast_message = self.format_message("message", {
                            "sender": client_name,
                            "room": client_room,
                            "text": 'Download has completed',
                        })
                        client_socket.send(broadcast_message.encode('utf-8'))

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
    server = Server('127.0.0.1', 12345)
    server.start()
