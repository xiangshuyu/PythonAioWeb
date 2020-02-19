import requests
from urllib.parse import urlencode
from requests.exceptions import RequestException
import re
import json
import time

base_url = 'https://m.weibo.cn/api/container/getIndex?'

headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2830678474',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'X-Request-With': 'XMLHttpRequest'
}


def get_page(page):
    params = {
        'type': 'uid',
        'value': '2830678474',
        'containerid': '1076032830678474',
        'page': page
    }
    url = base_url + urlencode(params)
    try:

        rsp = requests.get(url=url, headers=headers)
        if rsp.status_code == requests.codes.ok:
            return rsp.json()
    except requests.ConnectionError as e:
        print('Error', e.args)
        return None


def parse_json(json):
    if json:
        items = json.get('data').get('cards')


def main(offset=0):
    html = get_page(1)
    print(html)


if __name__ == '__main__':
    for i in range(1):
        main(offset=i * 10)
        time.sleep(1)
