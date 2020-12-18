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

home_address = os.getenv("HOME")
os.chdir(home_address)

json_load = load_json_file(f"{home_address}/export.json")

if __name__ == '__main__':
    if not (os.path.exists("generate_xlxs") and os.path.isdir("generate_xlxs")):
        os.mkdir("generate_xlxs")

    account_ids = json_load.get('items')
    data = []
    share_class_id = 4836
    share_series = 'Base Series'
    amount = [5500, 6000, 7000, 8000, 9000, 9500, 7500, 10000]
    date = ['01/01/2021', '02/01/2021', '03/01/2021', '04/01/2021']
    for i in range(0, account_ids.__len__()):
        acct_id = account_ids[i].get("acct_id")
        current_amount = amount[(i & amount.__len__() - 1)]
        current_date = date[(i & date.__len__() - 1)]
        data.append([acct_id, current_amount, current_date, share_class_id, share_series])

    sheetInfo = [
        SheetInfo(title=["Account ID", "Amount", "Effective Date", "Share Class", "Share Series Name"], rows=data)
    ]
    create_excel(ExcelFileInfo(sheet=sheetInfo, path=f"{home_address}/generate_xlxs/subscription_share.xlsx"))
