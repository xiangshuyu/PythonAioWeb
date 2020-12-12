# -*- coding:utf-8 -*-

import logging
import os
import sys
from functools import partialmethod

log_format = logging.Formatter(
    '%(asctime)s [%(filename)-20s] [%(threadName)-10s] [line:%(lineno)-3d] [%(levelname)-5s] | %(message)s')

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
file_dir = os.path.join(base_dir, 'log')

if not os.path.exists(file_dir):
    os.mkdir(file_dir)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(log_format)

info_file = os.path.join(file_dir, 'info.log')
info_file_handler = logging.FileHandler(info_file)
info_file_handler.setFormatter(log_format)

logger_info = logging.getLogger('logger_info')
logger_info.setLevel(logging.INFO)
logger_info.addHandler(info_file_handler)
logger_info.addHandler(stdout_handler)

error_file = os.path.join(file_dir, 'error.log')
error_file_handler = logging.FileHandler(error_file)
error_file_handler.setFormatter(log_format)

logger_error = logging.getLogger('logger_error')
logger_error.setLevel(logging.ERROR)
logger_error.addHandler(error_file_handler)
logger_error.addHandler(stdout_handler)


def format_dict(dic):
    if isinstance(dic, dict):
        return ', '.join('{}={}'.format(key, value)
                         for key, value in dic.items())
    elif isinstance(dic, str):
        return dic
    else:
        return dic.__str__()


def get_msg_str(msg):
    if isinstance(msg, dict):
        msg = format_dict(msg)
    return msg


class Logger(object):

    def __init__(self, name=None, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.addHandler(info_file_handler)
        self.logger.addHandler(error_file_handler)
        self.logger.addHandler(stdout_handler)

        self.debug = self.logger.debug
        self.info = self.logger.info
        self.warning = self.logger.warning
        self.error = self.logger.error
        self.critical = self.logger.critical
        self.exception = self.logger.exception

    def log(self, message, *args_dict, level=logging.INFO):
        if args_dict:
            self.logger.log(level=level,
                            msg=get_msg_str(message) + " " + format_dict(args_dict))
        else:
            self.logger.log(level=level, msg=message)

    def exception(self, msg, *args, **kwargs):
        self.logger.exception(msg, *args, exc_info=True, **kwargs)

    custom_debug = partialmethod(log, level=logging.DEBUG)

    custom_info = partialmethod(log, level=logging.INFO)

    custom_warn = partialmethod(log, level=logging.WARN)

    custom_error = partialmethod(log, level=logging.ERROR)

    custom_critical = partialmethod(log, level=logging.CRITICAL)


if __name__ == '__main__':
    logger_info.info("this is logger test")
    logger_error.error("this is error msg")
