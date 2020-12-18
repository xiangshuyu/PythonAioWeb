#!/usr/bin/python3
# -*- coding:utf-8 -*-

from multiprocessing import Process

from web import server
from util.hook_util import custom_sys_hook
from util.property_util import init_sys_prop, step_duplicate_prop

"""
    Since the GIL lock exist, We can use multi-process to run python server in a multi-core CPU
    
    We can use this server by the following way:
    ```
        python3 multi_server.py -p 8080 -p 8081
    ```
"""
if __name__ == '__main__':
    options = init_sys_prop()

    port_generator = step_duplicate_prop(options["port"])
    custom_sys_hook()

    for port in port_generator:
        current_options = dict()
        current_options.update(options)
        current_options["port"] = port

        process = Process(target=server, args=(current_options,))
        process.start()
