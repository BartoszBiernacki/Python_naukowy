import requests
from bs4 import BeautifulSoup
import json


def scrape() -> dict:
    url = 'https://www.kapitanbomba.pl/sklep/'
    html_content = requests.get(url).text

    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.find_all('div', class_="woocommerce-card__header")

    data = {}
    for element in elements:
        item = element.find('div', class_="woocommerce-loop-product__title")
        item_name = item.a['aria-label']
        item_price = element.find('span', class_='price')

        try:
            item_price = item_price.find_all('bdi')[-1]
        except IndexError:
            pass
        finally:
            item_price = item_price.text.replace('\xa0', ' ').strip()
            data[item_name] = item_price

    print(f'{url} scraped')
    return data


def save_json(data: dict, fdir: str) -> None:
    with open(fdir, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        print(f'{fdir} saved')

