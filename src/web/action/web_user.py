# -*- coding:utf-8 -*-

from src.web.frame.wrapper import *
from src.util.logger import with_logger, Logger

logger = Logger(__name__)


@with_logger(logger=logger)
@get("/login")
async def login():
    return ""
