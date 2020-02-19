# -*- coding:utf-8 -*-

from src.web.frame.wrapper import *
from src.web.filter.logger_filter import logger


@logger
@get("/login")
async def login():
    return ""