import time
import json
from pathlib import Path
import requests

# headers = {
#     'User-Agent': "User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"
# }
# params = {
#     'records_per_page': 50,
#     'page': 1,
# }
# url = 'https://5ka.ru/api/v2/special_offers/'
# response = requests.get(url, headers=headers)
#
# with open('5ka.html', 'w', encoding='UTF-8') as file:
#     file.write(response.text)


class StatusCodeError(Exception):
    def __init__(self, txt):
        self.txt = txt


class Parser5ka:
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"
    }
    _params = {
        'records_per_page': 50,
    }
    _headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
    }

    def __init__(self, start_url):
        self.start_url = start_url

    @staticmethod
    def _get_response(url, **kwargs):
        while True:
            try:
                response = requests.get(url, **kwargs)
                if response.status_code != 200:
                    raise StatusCodeError(f'status {response.status_code}')
                return response
            except (requests.exceptions.ConnectTimeout,
                    StatusCodeError):
                time.sleep(0.1)
    @staticmethod
    def _get(*args, **kwargs):
        while True:
            try:
                response = requests.get(*args, **kwargs)
                if response.status_code != 200:
                    raise StatusCodeError(f'status {response.status_code}')
                return response
            except (requests.exceptions.ConnectTimeout,
                    StatusCodeError):
                time.sleep(0.1)

    def run(self):
        for products in self.parse(self.start_url):
            for product in products:
                file_path = Path(__file__).parent.joinpath(f'{product["id"]}.json')
                self.save_file(file_path, product)
                self.save_to_json_file(product, product['id'])

    def parse(self, url):
        if not url:
            url = self.start_url
        params = self._params
        while url:
            response = self._get_response(url, headers=self.headers)
            response = self._get(url, params=params, headers=self._headers)
            if params:
                params = {}
            data: dict = response.json()
            url = data['next']
            yield data.get('results', [])
            url = data.get('next')

            yield data.get('results')

    def save_file(self, file_path: Path, data: dict):
        with open(file_path, 'w', encoding='UTF-8') as file:
            file.write(json.dumps(data))
            #json.dump(data, file, ensure_ascii=False)

    @staticmethod
    def save_to_json_file(data: dict, file_name):
        with open(f'products/{file_name}.json', 'w', encoding='UTF-8') as file:
            json.dump(data, file, ensure_ascii=False)


class ParserCatalog(Parser5ka):

    def __init__(self, start_url, category_url):
        self.category_url = category_url
        super().__init__(start_url)

    def get_categories(self, url):
        response = requests.get(url, headers=self._headers)
        return response.json()

    def run(self):
        for category in self.get_categories(self.category_url):
            data = {
                "name": category['parent_group_name'],
                'code': category['parent_group_code'],
                "products": [],
            }

            self._params['categories'] = category['parent_group_code']

            for products in self.parse(self.start_url):
                data["products"].extend(products)
            self.save_to_json_file(
                data,
                category['parent_group_code']
            )


if __name__ == '__main__':
    parser = ParserCatalog('https://5ka.ru/api/v2/special_offers/', 'https://5ka.ru/api/v2/categories/')
    parser.run()


