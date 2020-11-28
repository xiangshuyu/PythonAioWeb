#!/bin/bash

# the native freeze method by pip3
pip3 freeze > requirements.txt
pip3 install -r requirements.txt

# or you can use pipreqs module to freeze required modules
pip3 install pipreqs
pipreqs . --encoding=utf8 --force
pip3 install -r requirements.txt
