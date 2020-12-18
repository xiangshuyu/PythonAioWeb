import os
import sys

from util.excel.resolver import resolve_excel, ExcelResolveInfo, ExcelTable, unwrap_cell_obj
from util.excel.creator import ExcelFileInfo, SheetInfo, create_excel

glass_wall_head = {
    "Project": lambda x: x,
    "Task": lambda x: x[8:],
    "Status": lambda x: f" ({x})"
}


def generate_glass_wall(table: ExcelTable):
    xf_list = table.xf_list
    font_list = table.font_list
    head_used = {}
    for i, head in enumerate(list(map(unwrap_cell_obj, table.head))):
        if isinstance(head, str) and glass_wall_head.get(head):
            head_used[i] = head

    glass_wall_result = []
    for row in table:
        row_text = {}
        for i, cell_obj in enumerate(row):
            cell, xf = cell_obj
            font_index = xf_list[xf].font_index

            header = head_used.get(i)
            if not (font_list[font_index].weight == 700 and header) or not cell.value:
                continue
            row_text[header] = cell.value
        if not row_text.__len__() or row_text.__len__() != 3:
            continue
        glass_wall_result.append(row_text)
    return glass_wall_result


def generate_glass_wall_summary(table: ExcelTable):
    home_address = os.getenv("HOME")
    os.chdir(home_address)
    if not (os.path.exists("generate_xlxs") and os.path.isdir("generate_xlxs")):
        os.mkdir("generate_xlxs")
    data = generate_glass_wall(table)
    print(data)
