import xlrd
from xlrd.book import Book
from xlrd.sheet import Sheet, Cell
from xlrd.formatting import XF
from src.util.logger.logger import logger_info


class ExcelResolveInfo(object):

    def __init__(self, sheet=None, format_info=False, ):
        if sheet is None:
            sheet = []
        self.__sheet = sheet
        self.__format_info = format_info

    @property
    def sheet(self):
        return self.__sheet

    @property
    def format_info(self):
        return self.__format_info


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

    def check_col_num(self, index):
        return 0 < index < self.__cols

    def __iter__(self):
        return iter(self.__data)

    def __getitem__(self, item):
        data = self.__data
        if isinstance(item, int) and self.check_col_num(item):  # item是索引
            return [unwrap_cell_obj(data_item[item]) for data_item in data]
        if isinstance(item, slice):  # item是切片
            start = item.start
            stop = item.stop
            if start is None or not self.check_col_num(start):
                start = 0
            if stop is None or not self.check_col_num(stop):
                stop = 0
            return [list(map(unwrap_cell_obj, data_item[start:stop])) for data_item in data]

    def __getattr__(self, item):
        if self.__head.__contains__(item):
            return item


def unwrap_cell_obj(cell_obj):
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
    if isinstance(cell_obj, Cell):
        return cell_obj.value
    elif isinstance(cell_obj, tuple):
        cell, xf = cell_obj
        return unwrap_cell_obj(cell)
    else:
        return ''


def resolve_excel(file_path: str = "", params=ExcelResolveInfo(sheet=[1])):
    excel_data: Book = xlrd.open_workbook(filename=file_path, on_demand=True, formatting_info=params.format_info)
    logger_info.info("resolve excel : '%s', type : %s", file_path, excel_data)

    resolve_result = list()

    for sheet in params.sheet:
        if isinstance(sheet, str):
            sheet_table = excel_data.sheet_by_name(sheet_name=sheet)
        elif isinstance(sheet, int):
            sheet_table = excel_data.sheet_by_index(sheetx=sheet)
        else:
            continue
        result: ExcelTable = _resolve_sheet(sheet_table, excel_data)

        if isinstance(result, ExcelTable):
            resolve_result.append(result)

    return resolve_result


def _resolve_sheet(sheet_table: Sheet, book: Book):
    table_name = sheet_table.name
    sheet_rows = sheet_table.nrows
    sheet_cols = sheet_table.ncols

    logger_info.info("resolve sheet '%s',  rows : %s, cols: %s", table_name, sheet_rows, sheet_cols)

    result = ExcelTable(name=table_name, rows=sheet_rows, cols=sheet_cols)
    _config_excel_result(excel=result, book=book)

    for rowx in range(0, sheet_rows):
        row_data = list()
        for colx in range(0, sheet_cols):
            # get the Cell Object
            cell: Cell = sheet_table.col(colx, start_rowx=rowx, end_rowx=rowx + 1).__getitem__(0)
            # get the style of the Cell
            if sheet_table.formatting_info:
                row_data.append((cell, sheet_table.cell_xf_index(rowx, colx)))
            else:
                row_data.append(cell)

        if row_data:
            if not result.head:
                result.head = row_data
            else:
                result.data.append(row_data)

    return result


def _config_excel_result(excel: ExcelTable, book: Book):
    if book.formatting_info:
        excel.xf_list = book.xf_list
        excel.font_list = book.font_list
