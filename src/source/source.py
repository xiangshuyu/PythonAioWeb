# -*- coding: utf-8 -*-

from src.util.base_util import load_json_file
from src.project.env import base_dir
from peewee import *
import os


def all_db_info():
    all_db_file = os.path.join(os.path.join(base_dir, 'resource'), 'db_config.json')
    db_info = load_json_file(all_db_file)
    if isinstance(db_info, dict):
        active = db_info.get('db_active')
        info = db_info.get('db_info')
        return active, info
    else:
        raise AttributeError('this obj is not dict: %s' % type(db_info))


db_active, all_db_info = all_db_info()


def get_db_keys(all_db=all_db_info):
    return all_db.keys()


def mysql_db_info(db_key, all_db=all_db_info):
    if db_key is not None and get_db_keys().__contains__(db_key):
        db_info = all_db.get(db_key)
    else:
        db_info = all_db.get(db_active)
    return MySQLDatabase(**db_info)


def sqlite_db_info(name='asyncWeb.db'):
    db_path = os.path.join(base_dir, name)
    dbs = SqliteDatabase(db_path)
    return dbs


db = mysql_db_info(db_key=db_active, all_db=all_db_info)
