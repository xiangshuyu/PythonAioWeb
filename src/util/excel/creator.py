import xlwt
from xlwt import Worksheet

from src.util.logger.logger import logger_info


class SheetInfo(object):

    def __init__(self, name="", title=None, rows=None):
        if title is None or rows is None:
            raise RuntimeError("title and rows can't be null")

        self.__title = title
        self.__rows = rows
        self.__name = name

    def __iter__(self):
        return iter([self.__getattribute__(x) for x in self.__dict__])


class ExcelFileInfo(object):

    def __init__(self, sheet=None, path=""):
        if sheet is None:
            raise RuntimeError("sheet can't be null")

        self.__sheet = sheet
        self.__path = path

    @property
    def sheet(self):
        return self.__sheet

    @property
    def path(self):
        return self.__path

    def __iter__(self):
        return iter([self.__getattribute__(x) for x in self.__dict__])


def create_excel(file_info: ExcelFileInfo):
    if not isinstance(file_info, ExcelFileInfo):
        raise RuntimeError("file info should be an ExcelFileInfo")

    sheets, path = file_info
    logger_info.info("create excel : '%s'", path)

    workbook = xlwt.Workbook()
    for i in range(0, sheets.__len__()):
        sheet = sheets[i]
        if not isinstance(sheet, SheetInfo):
            continue

        title, rows, name = sheet
        if not name:
            name = f"sheet{i}"

        _create_sheet(title, rows, workbook.add_sheet(sheetname=name))

    workbook.save(path)


def _create_sheet(title, rows, sheet: Worksheet):
    for idx in range(0, title.__len__()):
        sheet.write(0, idx, title[idx])

    for x in range(0, rows.__len__()):
        row_data = rows[x]
        for y in range(0, row_data.__len__()):
            sheet.write(x + 1, y, row_data[y])


if __name__ == '__main__':
    data = []
    for i in range(0, 1000):
        account_name = f'new_recalc_account_{i + 1}'
        data.append([17674, 781181, account_name, 14256, 'Corporation'])

    sheetInfo = [
        SheetInfo(title=["Product ID", "Account Owner ID", "Account Name", "Account Terms ID", "Investor Type"],
                  rows=data)
    ]
    create_excel(ExcelFileInfo(sheet=sheetInfo, path="/home/stonkerxiang/doc/account.xlsx"))
