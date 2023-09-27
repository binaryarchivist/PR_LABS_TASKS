from bs4 import BeautifulSoup
import json
from pprint import pprint

from utils.utils import get_html_page
from functools import reduce


class InClass:
    def __init__(self, url):
        self.url = url

    def get_all_data(self):
        html_page = get_html_page(self.url)
        soup = BeautifulSoup(html_page, 'html.parser')
        wrapper = soup.select('nav.paginator > ul > li > a')

        links = []
        for a in wrapper:
            links.append('https://999.md' + a['href'])

        page_data = []

        for link in links:
            page_data.append(self.get_data(link))

        flatten_lists = reduce(lambda z, y: z + y, page_data)

        out_file = open("links.json", "w")
        json.dump(flatten_lists, out_file, indent=6)

        return set(flatten_lists)

    def get_data(self, url):
        html_page = get_html_page(url)
        soup = BeautifulSoup(html_page, 'html.parser')
        wrapper = soup.select('a.js-item-ad')

        links = []
        self.get_links_recursive(wrapper, links, len(wrapper) - 1)
        return links

    def get_links_recursive(self, wrapper, links, current_index):
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
            self.get_links_recursive(wrapper, links, current_index - 1)


in_class = InClass("https://999.md/ro/list/furniture-and-interior/furniture-fittings")

# pprint(len(in_class.get_all_data()))
pprint(in_class.get_all_data())