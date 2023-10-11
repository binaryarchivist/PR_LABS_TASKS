import os.path
import socket
import threading
import json
import base64
import uuid
from time import sleep

CHUNK_SIZE = 4096
files = {}


class Client:
    HOST = '127.0.0.1'
    PORT = 12345

    MSG_CONNECT = "connect"
    MSG_CONNECT_ACK = "connect_ack"
    MSG_MESSAGE = "message"
    MSG_UPLOAD = "upload"
    MSG_DOWNLOAD = "download"
    MSG_NOTIFICATION = "notification"

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_name = ""
        self.room_name = ""

    @staticmethod
    def is_file(string):
        return os.path.isfile(string)

    @staticmethod
    def format_message(msg_type, payload):
        """Formats the message to be sent as JSON."""
        return json.dumps({"type": msg_type, "payload": payload}, indent=2)

    def display_message(self, message_data):
        msg_type = message_data.get("type")
        payload = message_data.get("payload", {})

        if msg_type == self.MSG_CONNECT_ACK:
            print(f"Server: {payload.get('message')}")
        elif msg_type == self.MSG_MESSAGE:
            sender = payload.get("sender")
            text = payload.get("text")
            print(f"{sender}: {text}")
        elif msg_type == self.MSG_DOWNLOAD:
            binary = payload.get("binary")
            file_name = payload.get("file_name")

            with open(f'./media-client/{file_name}', 'ab') as file:
                decoded_chunk = base64.b64decode(binary)
                file.write(decoded_chunk)
                file.flush()

        elif msg_type == self.MSG_NOTIFICATION:
            print(f"Server Notification: {payload.get('message')}")

    def receive_messages(self):
        while True:
            message = self.client_socket.recv(8192).decode('utf-8')
            if not message:
                break
            try:
                message_data = json.loads(message)
                self.display_message(message_data)
            except json.JSONDecodeError:
                print("Received invalid JSON data.")

    def send_messages(self):
        while True:
            message_text = input("Enter a message (or 'exit' to quit): ")
            if message_text.lower() == 'exit':
                self.client_socket.close()
                break
            elif 'upload:' in message_text:
                message_text = message_text.replace('upload: ', '')
                if not self.is_file(message_text):
                    print(f'File {os.path.basename(message_text)} doesn\'t exist')
                    continue

                file_extension = os.path.basename(message_text).split('.')[1]
                file_name = str(uuid.uuid4()) + f'.{file_extension}'

                with open(message_text, "rb") as file:
                    chunk = file.read(CHUNK_SIZE)
                    while chunk:
                        base64_chunk = base64.b64encode(chunk)

                        message = self.format_message(self.MSG_UPLOAD, {
                            "sender": self.client_name,
                            "room": self.room_name,
                            "binary": base64_chunk.decode('utf-8'),
                            "file_name": file_name,
                            "is_completed": False
                        })

                        self.client_socket.send(message.encode('utf-8'))
                        sleep(1)
                        chunk = file.read(CHUNK_SIZE)
                    file.flush()
                    file.close()

                    message = self.format_message(self.MSG_UPLOAD, {
                        "sender": self.client_name,
                        "room": self.room_name,
                        "file_name": file_name,
                        "binary": '',
                        "is_completed": True
                    })
                    self.client_socket.send(message.encode('utf-8'))
            elif 'download:' in message_text:
                message_text = message_text.replace('download: ', '')
                file_name = os.path.basename(message_text)

                if os.path.exists(f'./media-client/{file_name}'):
                    print('File already exists.')
                    continue

                message = self.format_message(self.MSG_DOWNLOAD, {
                    "sender": self.client_name,
                    "room": self.room_name,
                    "file_name": file_name,
                })

                self.client_socket.send(message.encode('utf-8'))


            else:
                message = self.format_message(self.MSG_MESSAGE, {
                    "sender": self.client_name,
                    "room": self.room_name,
                    "text": message_text
                })
                self.client_socket.send(message.encode('utf-8'))

    def start(self):
        self.client_socket.connect((self.HOST, self.PORT))
        print(f"Connected to {self.HOST}:{self.PORT}")

        self.client_name = input("Enter your name: ")
        self.room_name = input("Enter room name: ")
        connect_message = self.format_message(self.MSG_CONNECT, {
            "name": self.client_name,
            "room": self.room_name
        })
        self.client_socket.send(connect_message.encode('utf-8'))

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        send_thread = threading.Thread(target=self.send_messages)
        send_thread.daemon = True
        send_thread.start()

        send_thread.join()
        receive_thread.join()


if __name__ == "__main__":
    client = Client()
    client.start()
