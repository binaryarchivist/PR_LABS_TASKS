'''
    scrap 999.md
    apartamente 3 etaje
'''
from bs4 import BeautifulSoup
import requests
from pprint import pprint


def get_html_page(url):
    html_page = requests.get(url)
    return html_page.text


def get_all_data(url):
    html_page = get_html_page(url)
    soup = BeautifulSoup(html_page, 'html.parser')
    wrapper = soup.select('nav.paginator > ul > li > a')

    links = []
    for a in wrapper:
        links.append('https://999.md' + a['href'])

    page_data = []

    for link in links:
        page_data.append(get_data(link))

    return page_data


def get_data(url):
    html_page = get_html_page(url)
    soup = BeautifulSoup(html_page, 'html.parser')
    wrapper = soup.select('a.js-item-ad')

    links = []
    get_links_recursive(wrapper, links, len(wrapper) - 1)
    return links


def get_links_recursive(wrapper, links, current_index):
    if current_index == 0:
        if 'booster' not in wrapper[current_index]['href']:
            new_link = 'https://999.md' + wrapper[current_index]['href']
            if new_link not in links:
                links.append(new_link)
            return
    else:
        if 'booster' not in wrapper[current_index]['href']:
            new_link = 'https://999.md' + wrapper[current_index]['href']
            if new_link not in links:
                links.append('https://999.md' + wrapper[current_index]['href'])
        get_links_recursive(wrapper, links, current_index - 1)





url = 'https://999.md/ro/list/construction-and-repair/stoves'
pprint(get_all_data(url))
