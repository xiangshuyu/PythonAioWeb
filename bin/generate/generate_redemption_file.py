#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

if __name__ == "__main__":
    file_folder = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(os.path.dirname(os.path.dirname(file_folder)), 'src'))
    sys.path.append(os.getcwd())

from util.base_util import load_json_file
from util.excel.creator import create_excel, ExcelFileInfo, SheetInfo

subscription_load = load_json_file("/home/stonkerxiang/export_sub.json")

if __name__ == '__main__':
    subscription_ids = subscription_load.get('items')
    data = []
    amount = [-500, -1000, -1200]
    date = ['02/01/2020', '03/31/2020', '04/30/2020',
            '05/31/2020', '06/30/2020', '07/31/2020', '08/31/2020']
    for i in range(0, subscription_ids.__len__()):
        subscription_ids_i_ = subscription_ids[i]
        trans_id = subscription_ids_i_.get("trans_id")
        acct_id = subscription_ids_i_.get("acct_id")
        current_amount = amount[(i & amount.__len__() - 1)]
        current_date = date[(i & date.__len__() - 1)]
        data.append([acct_id, current_amount, current_date, trans_id])

    sheetInfo = [
        SheetInfo(title=["Account ID", "Amount", "Effective Date", "Subscription ID"], rows=data)
    ]
    create_excel(ExcelFileInfo(sheet=sheetInfo, path="/home/stonkerxiang/doc/redemption.xlsx"))
