import time

from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from robot.robot_util import ImageParser

KEYWORD = '测试'
MAX_PAGE = 10
SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

browser = webdriver.Chrome(chrome_options=chrome_options)


# firefox_options = webdriver.FirefoxOptions()
# firefox_options.set_headless()
#
# browser = webdriver.Firefox(firefox_options=firefox_options)


def index_page(page):
    """
    抓取索引页
    :param page: 页码
    """
    print('正在爬取第', page, '页')
    try:
        url = 'https://www.jd.com'
        browser.get(url)
        search_bar = browser.find_element_by_id('key')
        search_bar.send_keys(KEYWORD)
        time.sleep(2)
        search_bar.send_keys(Keys.ENTER)

        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_goodsList .gl-warp .gl-item')))
        get_products()
    except TimeoutException as e:
        index_page(page)


def get_products():
    """
    提取商品数据
    """
    html = browser.page_source
    doc = pq(html)

    items = doc('#J_goodsList .gl-warp .gl-item').items()
    for item in items:
        product = {
            'image': item.find('.p-img .err-product').attr('data-lazy-img'),
            'price': item.find('.p-price').text().replace('\n', ''),
            'title': item.find('.p-name').text().replace('\n', '')
        }
        ImageParser().save_image(product)
        print(product)


def main():
    """
    遍历每一页
    """
    for i in range(1, 2):
        index_page(i)
    browser.close()


if __name__ == '__main__':
    main()
