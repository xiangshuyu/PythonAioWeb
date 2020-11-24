# -*- coding:utf-8 -*-

import json
import time
from datetime import datetime


def load_json_file(file):
    with open(file, "r+") as f:
        text = f.read()
        return json.loads(text)


# def unicode_to_utf8(value):
#     if isinstance(value, unicode):
#         value = value.encode("utf8")
#     return value


# 获取指定模块的所有方法
def step_module_func(mod):
    # 处理模块名
    if isinstance(mod, str):
        n = mod.rfind('.')
        if n == (-1):
            model = __import__(mod, globals(), locals())
        else:
            name = mod[n + 1:]
            package = __import__(mod[:n], globals(), locals(), [name])
            model = getattr(package, name)
    else:
        model = mod
    # 查看指定模块中的属性列表
    func_list = []
    for attr in dir(model):
        if attr.startswith('_'):
            continue
        func = getattr(model, attr)
        if callable(func):
            func_list.append(func)
    return func_list


def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:
        return u'%s小时前' % (delta // 3600)
    if delta < 604800:
        return u'%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)


def get_trace(distance, t):
    """
    :param distance: 位移量
    :param t: 计算间隔
    :return: 移动轨迹
    """
    if not isinstance(distance, int):
        return []
    if not isinstance(distance, float) \
            and not isinstance(distance, int):
        return []
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
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        trace.append(round(move))

    return trace
