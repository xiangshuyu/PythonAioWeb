# -*- coding:utf-8 -*-

import asyncio
import base64
import inspect
import os
from collections import Counter

from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet

from util.base_util import datetime_filter
from util.base_util import step_module_func
from util.logger import Logger
from web.frame.handler import RequestHandler
from web.frame.handler import ResponseHandler
from web.frame.resolver import init_jinja2

logger = Logger(__name__)


def add_static(app):
    path = os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 'static')
    app.router.add_static('/static/', path)
    logger.info('add static %s => %s' % ('/static/', path))


def add_route(app, fn):
    method = getattr(fn, '__method__', None)
    path = getattr(fn, '__route__', None)
    if path is None or method is None:
        raise ValueError('@get or @post not defined in %s.' % str(fn))
    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
        fn = asyncio.coroutine(fn)
    logger.info(
        'add route %s %s => %s(%s)' % (method, path, fn.__name__, ', '.join(inspect.signature(fn).parameters.keys())))
    app.router.add_route(method, path, RequestHandler(app, fn))


# 获取指定模块中的标志了@get, @post的方法
def add_routes(app, module_name):
    func_list = step_module_func(module_name)
    for func in func_list:
        method = getattr(func, '__method__', None)
        path = getattr(func, '__route__', None)
        if method and path:
            add_route(app, func)


def add_view_resolver(app, **kw):
    params = {"datetime": datetime_filter}
    params.update(kw)
    template = params.get("template", 'jinja2')
    env = {
        "jinja2": init_jinja2
    }[template](filters=params)
    app['__templating__'] = env


async def response_handler(app, handler):
    return ResponseHandler(app=app, handler=handler)


def session_handler():
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    return session_middleware(EncryptedCookieStorage(secret_key))
