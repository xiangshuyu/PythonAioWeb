#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess

if __name__ == "__main__":
    file_folder = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(file_folder))
    sys.path.append(os.getcwd())

from src.util.file_util import step_file_dir
from src.util.logger.logger import logger_info


def file_resolve_func(file):
    logger_info.info(file)
    subprocess.call(f"sed -i s#pcm#appapi.server#g {file}", shell=True,
                    executable="/bin/bash")


if __name__ == '__main__':
    step_file_dir('/home/stonkerxiang/java/AdminsProject/AdminsProject-appapi/src/main/java/com/talkweb/admins/appapi/server/webflux',
                  resolve=file_resolve_func)
