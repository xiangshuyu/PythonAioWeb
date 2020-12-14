#!/usr/bin/python
# -*- coding: utf-8 -*-
from source.source import db
from source.source import mysql_db_info
from source.source import get_db_keys

from util.logger.logger import Logger

logger = Logger(__name__)


def db_conn(sql, dbs=db):
    res_data = list()
    with dbs.connection_context():
        try:
            cursor = dbs.execute_sql(sql)
            cursor.execute(sql)

            for row in cursor:
                d = list()
                for r in row:
                    d.append(r)
                res_data.append(d)

            cursor.close()
        except Exception as e:
            logger.error("Mysql error %d: %s" % (e.args[0], e.args[1]))
            logger.error("Mysql error sql %s" % sql)

    return res_data


def db_conn_with_db_key(sql, key):
    if not key:
        return db_conn(sql=sql)
    else:
        logger.info("select db key: %s" % key)
        return db_conn(sql=sql, dbs=mysql_db_info(db_key=key))


def db_conn_all_db_key():
    return get_db_keys()
