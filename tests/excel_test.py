import os
import sys
from functools import reduce

if __name__ == "__main__":
    file_folder = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(file_folder))
    sys.path.append(os.getcwd())

from src.util.excel.resolver import resolve_excel, ExcelResolveInfo, ExcelTable, unwrap_cell_obj


def generate_glass_wall(table: ExcelTable):
    xf_list = table.xf_list
    font_list = table.font_list
    head_used = []
    for i, head in enumerate(list(map(unwrap_cell_obj, table.head))):
        if isinstance(head, str) and (head == 'Project' or head == 'Task' or head == 'Status'):
            head_used.append((i, head))
    head_index = list(map(lambda x: x[0], head_used))
    for row in table:
        row_text = []
        for i, cell_obj in enumerate(row):
            cell, xf = cell_obj
            font_index = xf_list[xf].font_index

            if not (font_list[font_index].weight == 700 and head_index.__contains__(i)) or not cell.value:
                continue
            row_text.append(cell.value)
        if not row_text.__len__():
            continue
        print(reduce(lambda x, y: x + '\t' + y, row_text))


def generate_glass_wall_summary():
    pass


# format_info=True will read the style of xls file.

# xlrd only support read the style for xls file.
# this will raise a NotImplementedError when used with an xlsx file.
excel = resolve_excel("/home/stonkerxiang/Downloads/B86_Accounts1.xls",
                      params=ExcelResolveInfo(sheet=[2], format_info=True))
excel_table: ExcelTable = excel[0]

generate_glass_wall(excel_table)
# xf_list = excel_table.xf_list
# font_list = excel_table.font_list
# list_ = xf_list[164]
# print(excel_table.head)
# for i in excel_table:
#     print(i)
#     print(list(map(lambda x: x[0].value, i)))
