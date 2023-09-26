from bs4 import BeautifulSoup
import requests
from pprint import pprint


def extract_numbers(string):
    result = ''
    for char in string:
        if char.isdigit():
            result = result + char
    return result

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


def get_general_info(soup):
    general = {}
    general_divs = soup.select(
        'div.adPage__content__inner > div.adPage__content__features > div.adPage__content__features__col')

    if general_divs:
        for general_div in general_divs:
            h2_tags = general_div.find_all('h2')

            for h2 in h2_tags:
                category = h2.text.lower().strip().replace(' ', '_')
                general[category] = {}

                ul = h2.find_next_sibling('ul')
                if ul:
                    unified_text = ''
                    for li in ul.find_all('li'):
                        if li['class'] == ['m-no_value']:
                            unified_text = unified_text + li.text + '\n'
                            general[category] = unified_text
                        else:
                            key_span = li.find('span', {'class': 'adPage__content__features__key'})
                            value_span = li.find('span', {'class': 'adPage__content__features__value'})

                            if key_span and value_span:
                                key_text = key_span.text.strip().lower().replace(' ', '_')
                                value_text = value_span.text.strip()

                                general[category][key_text] = value_text
    return general


def get_description(url):
    description = ''  # general description

    html_page = get_html_page(url)
    soup = BeautifulSoup(html_page, 'html.parser')
    desc_div = soup.find('div', class_='adPage__content__description')

    price_list = soup.find('ul', class_='adPage__content__price-feature__prices')
    prices = {}

    for price in price_list:
        if '€' in price.text:
            prices['euros'] = extract_numbers(price.text)
        elif '$' in price.text:
            prices['dollars'] = extract_numbers(price.text)
        elif 'lei' in price.text:
            prices['leis'] = extract_numbers(price.text)

    for str in desc_div:
        description = description + str

    return {
        'description': description,
        'features': get_general_info(soup),
        'prices': prices
    }


url = 'https://999.md/ro/list/construction-and-repair/stoves'

pprint(get_description('https://999.md/ro/83881851'))
