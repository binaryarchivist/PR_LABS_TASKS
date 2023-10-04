import socket
from pprint import pprint

from bs4 import BeautifulSoup

host = '127.0.0.1'
port = 3000


def get_html(path):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    curl = bytes(f'GET /{path} HTTP/1.1\nHost: {host}\n\n', 'utf-8')
    client.send(curl)
    client_response = client.recv(4096)
    str_response = str(client_response, 'utf-8')

    request_response, content = str_response.split('\n\n')

    return BeautifulSoup(content, 'lxml')


def get_products():
    soupcik = get_html('products')
    links = soupcik.findAll('a')

    product_db = []

    for link in links:
        link_soup = get_html(link['href'])
        span_tags = link_soup.findAll('span')

        product = {}
        for span in span_tags:
            if 'Name:' in span.text:
                product['name'] = span.text.strip('Name:')
            elif 'Author:' in span.text:
                product['author'] = span.text.strip('Author:')
            elif 'Description:' in span.text:
                product['description'] = span.text.strip('Description:')
            elif 'Price:' in span.text:
                product['price'] = span.text.strip('Price:')

        product_db.append(product)

    return product_db


result = {
    'home': get_html('home'),
    'about': get_html('description'),
    'contacts': get_html('contacts'),
    'products': get_products()
}

pprint(result)
