import json
import socket
import signal
import sys
import re

HOST = '127.0.0.1'
PORT = 3003

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(5)  # Backlog for multiple simultaneous connections
print(f"Server is listening on {HOST}:{PORT}")


def signal_handler(sig, frame):
    print("\nShutting down the server...")
    server_socket.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def handle_request(client_socket):
    request_data = client_socket.recv(1024).decode('utf-8')
    print(f"Received Request:\n{request_data}")

    request_lines = request_data.split('\n')
    request_line = request_lines[0].strip().split()

    method = request_line[0]
    path = request_line[1]

    response_content = ''
    status_code = 200

    file = open('./mocks/products.json')
    products: list = json.load(file)

    # Define a simple routing mechanism
    if path == '/home':
        response_content = 'Hello, World!'
    elif path == '/about':
        response_content = 'This is the About page.'
    elif path == '/contacts':
        response_content = 'This is the Contacts page.'
    elif path == '/products':
        response_content = ''
        for i, product in enumerate(products):
            response_content += f'<a href="product/{i}">{product["name"]}</a><br/>'
    elif re.match('/product/\d', path):
        t = ''
        for char in path:
            if char.isnumeric():
                t += char

        if int(t) < len(products):
            response_content = f'<div style="display: flex; flex-direction: column; gap: 2px"><span>Name: f{products[int(t)]["name"]}</span><span>Author: f{products[int(t)]["author"]}</span><span>Price: f{products[int(t)]["price"]}</span>  <span>Description: f{products[int(t)]["description"]}</span> </div>'
        else:
            response_content = f'404 Not Found {t}'
            status_code = 404
    else:
        response_content = '404 Not Found'
        status_code = 404
    response = f'HTTP/1.1 {status_code} OK\nContent-Type: text/html\n\n{response_content}'

    client_socket.send(response.encode('utf-8'))
    client_socket.close()


while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    try:
        handle_request(client_socket)
    except KeyboardInterrupt:
        pass
