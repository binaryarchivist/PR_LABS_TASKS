from bs4 import BeautifulSoup
from pprint import pprint

from utils.utils import get_html_page, extract_numbers


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
    description = ''

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

    for sentence in desc_div:
        description = description + sentence

    return {
        'description': description,
        'features': get_general_info(soup),
        'prices': prices
    }


url = 'https://999.md/ro/list/construction-and-repair/stoves'

pprint(get_description('https://999.md/ro/83881851'))
