#!/usr/bin/python3
# -*- coding:utf-8 -*-

import asyncio
import threading
import sys

from aiohttp import web

from src.util.logger.logger import logger_info
from src.web.frame.dispatcher import add_routes
from src.web.frame.dispatcher import add_static
from src.web.frame.dispatcher import add_view_resolver
from src.web.frame.dispatcher import response_handler
from src.web.frame.dispatcher import session_handler

from src.web import web_handlers


async def init(event_loop, port=9090, host='0.0.0.0'):
    app = web.Application(loop=event_loop, middlewares=[session_handler(), response_handler])

    add_static(app=app)

    for web_handler in web_handlers:
        add_routes(app=app, module_name=web_handler)

    add_view_resolver(app=app)

    app_runner = web.AppRunner(app)
    await app_runner.setup()
    srv = await event_loop.create_server(app_runner.server, host, port)
    logger_info.info("server started at http://%s:%s...'" % (host, port))
    return srv


if __name__ == '__main__':
    thread = threading.current_thread()

    logger_info.info("thread id: %s, name: %s" % (thread.ident, thread.name))
    logger_info.info(f"python3 path in {sys.path}")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()
