# -*- coding:utf-8 -*-

from web.frame.wrapper import *
from util.logger import with_logger, Logger

logger = Logger(__name__)


@with_logger(logger=logger)
@get("/login")
async def login():
    return ""
