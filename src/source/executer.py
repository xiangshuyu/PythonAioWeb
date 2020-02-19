#!/usr/bin/python
# -*- coding: utf-8 -*-
from src.source.source import db
from src.source.source import mysql_db_info
from src.source.source import get_db_keys

from src.util.logger.logger import logger_error
from src.util.logger.logger import logger_info


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
            logger_error.error("Mysql error %d: %s" % (e.args[0], e.args[1]))
            logger_error.error("Mysql error sql %s" % sql)

    return res_data


def db_conn_with_db_key(sql, key):
    if not key:
        return db_conn(sql=sql)
    else:
        logger_info.info("select db key: %s" % key)
        return db_conn(sql=sql, dbs=mysql_db_info(db_key=key))


def db_conn_all_db_key():
    return get_db_keys()
