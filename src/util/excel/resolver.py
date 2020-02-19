import xlrd
from xlrd.sheet import Sheet, Cell
from src.util.logger.logger import logger_info

class ExcelResolveInfo(object):

    def __init__(self, sheet=None, ):
        if sheet is None:
            sheet = []
        self.__sheet = sheet

    @property
    def sheet(self):
        return self.__sheet


class ExcelTable(object):

    def __init__(self, name='', rows=0, cols=0, head=None, data=None):
        if data is None:
            data = []
        if head is None:
            head = []
        self.__name = name
        self.__rows = rows
        self.__cols = cols
        self.__head = head
        self.__data = data

    @property
    def head(self):
        return self.__head

    @head.setter
    def head(self, head):
        if not isinstance(head, list):
            raise ValueError('score must be an integer!')
        self.__head = head

    @property
    def data(self):
        return self.__data

    def check_index(self, index):
        return 0 < index < self.__cols

    def __iter__(self):
        return self.__data

    def __next__(self):
        return self.__data[0]

    def __getitem__(self, item):
        data = self.__data
        if isinstance(item, int) and self.check_index(item):  # item是索引
            return [resolve_cell(data_item[item]) for data_item in data]
        if isinstance(item, slice):  # item是切片
            start = item.start
            stop = item.stop
            if start is None or not self.check_index(start):
                start = 0
            if stop is None or not self.check_index(stop):
                stop = 0
            return [list(map(resolve_cell, data_item[start:stop])) for data_item in data]

    def __getattr__(self, item):
        if self.__head.__contains__(item):
            return item


def resolve_excel(file_path: str = "", params=ExcelResolveInfo()):
    excel_data = xlrd.open_workbook(file_path)
    logger_info.info("resolve excel : '%s', type : %s", file_path, excel_data)

    resolve_result = list()

    for sheet in params.sheet:
        if isinstance(sheet, str):
            sheet_table = excel_data.sheet_by_name(sheet_name=sheet)
        elif isinstance(sheet, int):
            sheet_table = excel_data.sheet_by_index(sheetx=sheet)
        else:
            continue
        result = resolve_sheet(sheet_table, params)

        if isinstance(result, ExcelTable):
            resolve_result.append(result)

    return resolve_result


def resolve_sheet(sheet_table, params=ExcelResolveInfo()):
    table_name = sheet_table.name
    sheet_rows = sheet_table.nrows
    sheet_cols = sheet_table.ncols
    logger_info.info("resolve sheet '%s',  rows : %s, cols: %s", table_name, sheet_rows, sheet_cols)

    result = ExcelTable(name=table_name, rows=sheet_rows, cols=sheet_cols)

    for rowx in range(0, sheet_rows):
        row_data = list()
        for colx in range(0, sheet_cols):
            row_col = sheet_table.col(colx, start_rowx=rowx, end_rowx=rowx + 1).__getitem__(0)
            if row_col.value:
                row_data.append(row_col)

        if row_data:
            if not result.head:
                result.head = row_data
            else:
                result.data.append(row_data)

    return result


def resolve_cell(cell):
    """
    ctype_text = {
        XL_CELL_EMPTY: 'empty',
        XL_CELL_TEXT: 'text',
        XL_CELL_NUMBER: 'number',
        XL_CELL_DATE: 'xldate',
        XL_CELL_BOOLEAN: 'bool',
        XL_CELL_ERROR: 'error',
        XL_CELL_BLANK: 'blank',
    }
    """
    if not isinstance(cell, Cell):
        return ''
    cell_ctype = cell.ctype
    return cell.value
