from typing import Optional

import xlwt
from xlwt import Worksheet, XFStyle

from util.logger.logger import Logger

logger = Logger(__name__)


class SheetCell(object):

    def __init__(self, label: str = "",
                 style: Optional[XFStyle] = None, cell_type: str = "",
                 extra: Optional[dict] = None):
        if extra is None:
            extra = {}
        self.__label = _cell_type[cell_type](label, extra)
        self.__style = style

    def __iter__(self):
        return iter([self.__getattribute__(x) for x in self.__dict__])


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
    logger.info("create excel : '%s'", path)

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
            cell = row_data[y]
            if not isinstance(cell, SheetCell):
                sheet.write(x + 1, y, cell)
            else:
                label, style = cell
                if not style:
                    sheet.write(x + 1, y, label)
                elif isinstance(style, XFStyle):
                    sheet.write(x + 1, y, label, style)


_cell_type = {
    "": lambda x, extra: x,
    "hyperlink": lambda x, extra: xlwt.Formula(f'HYPERLINK("{extra["hyperlink"]}","{x}")')
}

if __name__ == '__main__':
    data = []
    for i in range(0, 1000):
        account_name = f'new_recalc_account_{i + 1}'
        data.append([17674, 781181, account_name, 14256, 'Corporation',
                     SheetCell(label="test", cell_type="hyperlink", extra={"hyperlink": "https://www.baidu.com"})])

    sheetInfo = [
        SheetInfo(
            title=["Product ID", "Account Owner ID", "Account Name", "Account Terms ID", "Investor Type", "Hyperlink"],
            rows=data)
    ]
    create_excel(ExcelFileInfo(sheet=sheetInfo, path="/home/stonkerxiang/doc/account.xlsx"))
