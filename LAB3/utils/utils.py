import requests


def get_html_page(url):
    html_page = requests.get(url)
    return html_page.text


def extract_numbers(string):
    result = ''
    for char in string:
        if char.isdigit():
            result = result + char
    return result
