#!/bin/bash
import cx_Oracle as Oracle

db = Oracle.connect('WZSC/TWWZ@2015@192.168.2.10:1521/TWWZSC')
cursor = db.cursor()

# execute sql
cursor.execute('select * from v_dc_ricer_produce_data where c_product_id = 3473416 order by c_producedate desc')
data = cursor.fetchall()

for d in data:
    print('Database time:%s' % data)

# close cursor and oracle
cursor.close()
db.close()
