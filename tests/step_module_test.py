#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import json

if __name__ == "__main__":
    file_folder = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(file_folder))
    sys.path.append(os.getcwd())

from src.util.base_util import step_module_func

print(step_module_func(json))
print("\n")
print(step_module_func('src.web.action.web_index'))
