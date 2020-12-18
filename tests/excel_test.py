import os
import sys
from functools import reduce

if __name__ == "__main__":
    file_folder = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(os.path.dirname(file_folder), 'src'))
    sys.path.append(os.getcwd())

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

    common_data = ['B86-Account', 'b86']
    table_data = generate_glass_wall(table)

    excel_data = []
    for data in table_data:
        result = [*common_data]
        
        excel_data.append(result)

    sheetInfo = [
        SheetInfo(title=["Team", "Glasswall tag", "Glasswall Item", "Notes", "Jira"],
                  rows=excel_data)
    ]
    create_excel(ExcelFileInfo(sheet=sheetInfo, path=f"{home_address}/generate_xlxs/glasswall.xlsx"))


# format_info=True will read the style of xls file.

# xlrd only support read the style for xls file.
# this will raise a NotImplementedError when used with an xlsx file.
excel = resolve_excel("/home/stonkerxiang/temp/glasswallx/B86_Accounts_09_28.xls",
                      params=ExcelResolveInfo(sheet=[2], format_info=True))
excel_table: ExcelTable = excel[0]

print("glasswall web text:")
glass_wall = generate_glass_wall(excel_table)
for text in glass_wall:
    text_list = []
    for k, v in text.items():
        render_func = glass_wall_head.get(k)
        if callable(render_func):
            text_list.append(render_func(v))
        else:
            text_list.append(v)
    print(" -".join(text_list))

print("\nglasswall summary text:")
generate_glass_wall_summary(excel_table)

# xf_list = excel_table.xf_list
# font_list = excel_table.font_list
# list_ = xf_list[164]
# print(excel_table.head)
# for i in excel_table:
#     print(i)
#     print(list(map(lambda x: x[0].value, i)))
