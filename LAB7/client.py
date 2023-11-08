import os.path
import socket
import threading
import json
import pika

CHUNK_SIZE = 4096
files = {}


class Client:
    HOST = '127.0.0.1'
    PORT = 12345

    MSG_CONNECT = "connect"
    MSG_CONNECT_ACK = "connect_ack"
    MSG_MESSAGE = "message"
    MSG_NOTIFICATION = "notification"

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.client_queue = ''
        self.client_name = ""
        self.room_name = ""

        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

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
            if payload['room'] == self.room_name and payload['sender'] != self.client_name:
                sender = payload.get("sender")
                text = payload.get("text")
                print(f"{sender}: {text}")
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
            message_text = input()
            if message_text.lower() == 'exit':
                self.client_socket.close()
                break
            else:
                message = self.format_message(self.MSG_MESSAGE, {
                    "sender": self.client_name,
                    "room": self.room_name,
                    "text": message_text
                })
                self.channel.basic_publish(exchange='',
                                           routing_key=self.client_queue,
                                           body=message.encode('utf-8'))

    def start(self):
        self.client_socket.connect((self.HOST, self.PORT))
        host, port = self.client_socket.getsockname()
        self.client_queue = ''.join([str(host), ':', str(port)])

        print(f"Connected to {self.HOST}:{self.PORT}")

        self.client_name = input("Enter your name: ")
        self.room_name = input("Enter room name: ")

        self.channel.queue_declare(queue=self.client_queue)

        connect_message = self.format_message(self.MSG_CONNECT, {
            "name": self.client_name,
            "room": self.room_name
        })

        self.channel.basic_publish(exchange='',
                                   routing_key=self.client_queue,
                                   body=connect_message.encode('utf-8'))

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
