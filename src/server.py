#!/usr/bin/python3
# -*- coding:utf-8 -*-

from web import server
from util.hook_util import custom_sys_hook
from util.property_util import init_sys_prop, filter_duplicate_prop

if __name__ == '__main__':
    options = init_sys_prop()

    filter_duplicate_prop(options, "port")

    custom_sys_hook()
    server(options=options)
