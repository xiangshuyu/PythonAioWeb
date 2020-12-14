#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import json

if __name__ == "__main__":
    file_folder = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(os.path.dirname(file_folder), 'src'))
    sys.path.append(os.getcwd())

from util.base_util import step_module_func

print(step_module_func(json))
print("\n")
print(step_module_func('web.action.web_index'))
