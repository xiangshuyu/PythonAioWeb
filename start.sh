#!/bin/bash
cd `dirname $0`
lsof -i:9090 | grep -v PID | awk '{print $2}'| xargs kill -9
#sed  "27,29s#Dev#Prod#g"  config/db.json
python ./server.py > ./dbs.out 2>&1 &
