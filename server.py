#!/usr/bin/python3
# -*- coding:utf-8 -*-

import asyncio
import threading
import sys

from aiohttp import web
from aiohttp.web import Application, AppRunner

from src.util.logger.logger import logger_info
from src.util.property_util import init_sys_prop

from src.web.frame import *
from src.web.action import web_handlers


async def init(event_loop, port: int = 9090, host: str = '0.0.0.0', **kw):
    app: Application = web.Application(loop=event_loop, middlewares=[session_handler(), response_handler])

    add_static(app=app)

    for web_handler in web_handlers:
        add_routes(app=app, module_name=web_handler)

    add_view_resolver(app=app)

    app_runner: AppRunner = web.AppRunner(app)
    await app_runner.setup()
    srv = await event_loop.create_server(app_runner.server, host, port)
    logger_info.info("server started at http://%s:%s...'" % (host, port))
    return srv


if __name__ == '__main__':
    thread = threading.current_thread()

    options = init_sys_prop()

    logger_info.info("thread id: %s, name: %s" % (thread.ident, thread.name))
    logger_info.info(f"python3 path: {sys.path}")
    logger_info.info(f"system get props: {options}")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop, **options))
    loop.run_forever()
