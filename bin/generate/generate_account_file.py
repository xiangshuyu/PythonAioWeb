
import os
import sys

if __name__ == "__main__":
    file_folder = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(os.path.dirname(os.path.dirname(file_folder)), 'src'))
    sys.path.append(os.getcwd())

from util.excel.creator import create_excel, ExcelFileInfo, SheetInfo


if __name__ == '__main__':
    home_address = os.getenv("HOME")
    os.chdir(home_address)
    if not (os.path.exists("generate_xlxs") and os.path.isdir("generate_xlxs")):
        os.mkdir("generate_xlxs")
    data = []
    for i in range(0, 500):
        account_name = f'new_recalc_account_{i + 1}'
        data.append([16788, 810185, account_name, 13360, 'Corporation'])

    sheetInfo = [
        SheetInfo(title=["Product ID", "Account Owner ID", "Account Name", "Account Terms ID", "Investor Type"],
                  rows=data)
    ]
    create_excel(ExcelFileInfo(sheet=sheetInfo, path=f"{home_address}/generate_xlxs/account11.xlsx"))
