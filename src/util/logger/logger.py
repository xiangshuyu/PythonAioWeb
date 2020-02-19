# -*- coding:utf-8 -*-

import logging
import os
import sys

log_format = logging.Formatter('%(asctime)s [%(filename)-20s] [line:%(lineno)-3d] [%(levelname)-5s] | %(message)s')

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
file_dir = os.path.join(base_dir, 'log')

if not os.path.exists(file_dir):
    os.mkdir(file_dir)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(log_format)

info_file = os.path.join(file_dir, 'info.log')
info_file_handler = logging.FileHandler(info_file)
info_file_handler.setFormatter(log_format)
logger_info = logging.getLogger('info')
logger_info.setLevel(logging.INFO)
logger_info.addHandler(info_file_handler)
logger_info.addHandler(stdout_handler)

error_file = os.path.join(file_dir, 'error.log')
error_file_handler = logging.FileHandler(error_file)
error_file_handler.setFormatter(log_format)
logger_error = logging.getLogger('error')
logger_error.setLevel(logging.ERROR)
logger_error.addHandler(error_file_handler)

if __name__ == '__main__':
    logger_info.info("this is logger test")
    logger_error.error("this is error msg")
