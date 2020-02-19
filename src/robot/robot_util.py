import os
import time
from hashlib import md5

import requests
from requests import codes
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class MoveGap(object):

    def __init__(self, distance: int, time_internal):
        """
        :param distance: 位移量
        :param time_internal: 计算间隔
        """
        if not isinstance(distance, int):
            raise AttributeError('distance should be int')
        if not isinstance(time_internal, float) \
                and not isinstance(time_internal, int):
            raise AttributeError('time_internal should be int or float')

        self._distance = distance
        self._time_internal = time_internal

    def __call__(self, *args, **kwargs):

        browser = kwargs.get('browser')
        slider = kwargs.get('slider')

        if not isinstance(browser, WebDriver):
            raise AttributeError('browser should be WebDriver object')

        if not isinstance(slider, WebElement):
            raise AttributeError('slider should be WebElement object')

        tracks = self._get_tracks()
        self._move_to_gap(browser=browser, slider=slider, tracks=tracks)

    def _get_tracks(self) -> list:
        distance = self._distance
        time_internal = self._time_internal
        trace = []
        current = 0
        mid = distance * 4 / 5
        v = 0

        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3
            v0 = v
            v = v0 + a * time_internal
            move = v0 * time_internal + 1 / 2 * a * time_internal * time_internal
            current += move
            trace.append(round(current))

        return trace

    @staticmethod
    def _move_to_gap(browser, slider, tracks):
        print(tracks)
        ActionChains(browser).click_and_hold(slider).perform()
        for x in tracks:
            ActionChains(browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(browser).release().perform()


class ImageParser(object):

    @staticmethod
    def save_image(item):
        img_path = 'img' + os.path.sep + item.get('title')
        if not os.path.exists(img_path):
            os.makedirs(img_path)
        try:
            image = item.get('image')
            if not image:
                return
            if not str(image).startswith('http'):
                image = 'http:' + image
            resp = requests.get(image)
            if codes.ok == resp.status_code:
                file_path = img_path + os.path.sep + '{file_name}.{file_suffix}'.format(
                    file_name=md5(resp.content).hexdigest(), file_suffix='jpg')
                if not os.path.exists(file_path):
                    with open(file_path, 'wb') as f:
                        f.write(resp.content)
                    print('Downloaded image path is %s' % file_path)
                else:
                    print('Already Downloaded', file_path)
        except requests.ConnectionError:
            print('Failed to Save Image，item %s' % item)
