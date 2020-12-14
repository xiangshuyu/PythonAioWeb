from urllib.parse import quote

from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from robot.robot_util import MoveGap
import time

KEYWORD = 'ipad'
MAX_PAGE = 10
SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')

browser = webdriver.Chrome(chrome_options=chrome_options)


def index_page(page):
    """
    抓取索引页
    :param page: 页码
    """
    print('正在爬取第', page, '页')
    try:
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
        browser.get(url)

        while True:
            login_switch = browser.find_element_by_css_selector(".login-switch")
            if not login_switch:
                break
            login_switch.click()
            username = browser.find_element_by_id('TPL_username_1')
            password = browser.find_element_by_id('TPL_password_1')
            submit = browser.find_element_by_id('J_SubmitStatic')

            username.send_keys('15200822495')
            password.send_keys('asd8513692')
            time.sleep(1)

            slider = browser.find_element_by_id('nc_1_n1z')
            MoveGap(300, 1)(1, 2, browser=browser, slider=slider)
            time.sleep(1)

            submit.click()

        wait = WebDriverWait(browser, 10)
        if page > 1:
            input_page = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
            input_page.clear()
            input_page.send_keys(page)
            submit.click()

        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
        get_products()
    except TimeoutException as e:
        index_page(page)


def get_products():
    """
    提取商品数据
    """
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
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
