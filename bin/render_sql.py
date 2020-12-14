#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

if __name__ == "__main__":
    file_folder = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(os.path.dirname(file_folder), 'src'))
    sys.path.append(os.getcwd())

from util.excel.resolver import resolve_excel, ExcelResolveInfo
from util.random_util import gen_random_str
from datetime import datetime, timedelta, date


def render_to_sql(params):
    dateTime = datetime.now()
    today_timedelta_days_ = dateTime.today() + timedelta(days=90)
    date_time_strftime = dateTime.strftime("%Y-%m-%d %H:%M:%S")
    expire_time_strftime = today_timedelta_days_.strftime("%Y-%m-%d %H:%M:%S")
    random_str = gen_random_str(32)
    sql = "insert into `account`(`gmt_create`,`gmt_modified`,`account_id`,`username`,`phone_number`,`password`," \
          "`status`,`is_deleted`,`type`,`expire_time`) values('%s','%s','%s','%s','%s'," \
          "'123456',1,0,3,'%s');" % (
              date_time_strftime, date_time_strftime, random_str, params[1], params[0], expire_time_strftime)

    # sql = "update `account` set expire_time = '%s' where phone_number = '%s' and username= '%s';" % (
    #    expire_time_strftime, params[0], params[1])

    return sql


if __name__ == '__main__':
    param = ExcelResolveInfo(sheet=[1])
    excel = resolve_excel('/home/stonkerxiang/Documents/csu-20200217.xlsx', param)
    excel_table = excel[0]
    for i in excel_table:
        print(i)

    l = list(map(render_to_sql, excel_table[3:5]))

    with open('./insert1.sql', 'w', encoding='utf-8') as f:
        for i in l:
            f.write("%s\n" % i)
    print(sys.path)
