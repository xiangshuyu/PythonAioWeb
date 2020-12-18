import os
import sys
import time

if __name__ == "__main__":
    file_folder = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(os.path.dirname(os.path.dirname(file_folder)), 'src'))
    sys.path.append(os.getcwd())

from source.source import mysql_db_info

mysql_database = mysql_db_info("adminLocal")

query_status = "show global status like \"%innodb%\";"


def execute_monitor():
    cursor = mysql_database.cursor()
    cursor.execute(query_status)
    result = dict()
    for i in cursor:
        if isinstance(i, tuple):
            print(i)
            name, val = i
            result[name] = val
    return result


if __name__ == '__main__':
    while True:
        print(execute_monitor())
        time.sleep(1)

