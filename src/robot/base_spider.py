import requests
from requests.exceptions import RequestException
import re
import json
import time


def get_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
        }
        rsp = requests.get(url=url, headers=headers)
        if rsp.status_code == requests.codes.ok:
            return rsp.text
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.'
        '*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',
        re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6],
        }


def main(offset=0):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_page(url)
    for item in parse_one_page(html):
        print(item)


if __name__ == '__main__':
    for i in range(5):
        main(offset=i * 10)
        time.sleep(1)
