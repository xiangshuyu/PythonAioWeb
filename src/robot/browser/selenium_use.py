import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def inputs():
    browser = webdriver.Chrome()
    try:
        browser.get("https://www.baidu.com")
        input_item = browser.find_element_by_id('kw')
        input_item.send_keys('iphone')
        time.sleep(2)
        input_item.clear()
        input_item.send_keys('Python')
        time.sleep(2)
        input_item.send_keys(Keys.ENTER)

        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'content_left')))

        print(browser.current_url)
        print(browser.get_cookies())
        print(browser.page_source)
    finally:
        browser.close()


def action_chain():
    browser = webdriver.Chrome()
    browser.get("http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable")
    browser.switch_to.frame('iframeResult')
    source = browser.find_element_by_css_selector('#draggable')
    target = browser.find_element_by_css_selector('#droppable')

    actions = ActionChains(browser)
    actions.drag_and_drop(source=source, target=target)
    actions.perform()
    time.sleep(2)


def node():
    browser = webdriver.Chrome()
    browser.get("https://www.taobao.com")
    input_first = browser.find_element_by_id('q')
    input_second = browser.find_element_by_css_selector('#q')
    input_third = browser.find_element_by_xpath('//*[@id="q"]')
    print(input_first)
    print(input_second)
    print(input_third)

    print(input_first.get_attribute('class'))
    print(input_first.text)
    print(input_first.location)

    li = browser.find_element_by_css_selector('.service-bd li')
    print(li)

    lis = browser.find_elements_by_css_selector('.service-bd li')
    print(lis)
    browser.close()


def execute_js():
    browser = webdriver.Chrome()
    browser.get("https://www.zhihu.com/explore")
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    browser.execute_script('window.alert(window.navigator.webdriver)')

    wait = WebDriverWait(browser, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn search')))


def cookies():
    browser = webdriver.Chrome()
    browser.get("https://www.zhihu.com/explore")
    print(browser.get_cookies())
    browser.add_cookie({'name': 'name', 'domain': 'www.zhihu.com', 'value': 'germey'})
    print(browser.get_cookies())
    browser.delete_all_cookies()
    print(browser.get_cookies())


def add_handle():
    browser = webdriver.Chrome()
    browser.get("https://search.jd.com/Search?keyword=ipad")
    browser.execute_script('window.open()')
    print(browser.window_handles)
    browser.switch_to.window(browser.window_handles[1])
    browser.get("https://www.taobao.com")
    time.sleep(2)
    browser.switch_to.window(browser.window_handles[0])
    browser.get('http://python.org')
    time.sleep(2)


if __name__ == '__main__':
    execute_js()
