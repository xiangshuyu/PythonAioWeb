#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess

if __name__ == "__main__":
    file_folder = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(os.path.dirname(file_folder), 'src'))
    sys.path.append(os.getcwd())

from util.file_util import step_file_dir


def file_resolve_func(file):
    print(file)
    subprocess.call(f"sed -i s#com.talkweb.admins.core.base.BasicModel#com.sharework.micro.common.basic.BasicModel#g {file}", shell=True,
                    executable="/bin/bash")


if __name__ == '__main__':
    step_file_dir('/home/xsy/java/AdminsProject/AdminsProject-appapi', resolve=file_resolve_func)
    step_file_dir('/home/xsy/java/AdminsProject/AdminsProject-common', resolve=file_resolve_func)
    step_file_dir('/home/xsy/java/AdminsProject/AdminsProject-consumer', resolve=file_resolve_func)
    step_file_dir('/home/xsy/java/AdminsProject/AdminsProject-core', resolve=file_resolve_func)
    step_file_dir('/home/xsy/java/AdminsProject/AdminsProject-core-api', resolve=file_resolve_func)
    step_file_dir('/home/xsy/java/AdminsProject/AdminsProject-h5', resolve=file_resolve_func)
    step_file_dir('/home/xsy/java/AdminsProject/AdminsProject-op', resolve=file_resolve_func)
    step_file_dir('/home/xsy/java/AdminsProject/AdminsProject-pcm', resolve=file_resolve_func)
    step_file_dir('/home/xsy/java/AdminsProject/AdminsProject-rest', resolve=file_resolve_func)
    step_file_dir('/home/xsy/java/AdminsProject/AdminsProject-script', resolve=file_resolve_func)
    step_file_dir('/home/xsy/java/AdminsProject/AdminsProject-test', resolve=file_resolve_func)
    step_file_dir('/home/xsy/java/AdminsProject/AdminsProject-thirdpart', resolve=file_resolve_func)
    step_file_dir('/home/xsy/java/AdminsProject/AdminsProject-webapp', resolve=file_resolve_func)
