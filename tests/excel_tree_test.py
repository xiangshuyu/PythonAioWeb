import json
import os
import sys

if __name__ == "__main__":
    file_folder = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(os.path.dirname(file_folder), 'src'))
    sys.path.append(os.getcwd())

from util.excel.resolver import resolve_excel, ExcelResolveInfo, ExcelTable, unwrap_cell_obj

excel = resolve_excel("/home/stonkerxiang/Downloads/族库目录.xlsx",
                      params=ExcelResolveInfo(sheet=[0]))

excel_table: ExcelTable = excel[0]

result = []
for i, row in enumerate(excel_table):
    if i == 0:
        continue
    for j, cell in enumerate(row):
        val = unwrap_cell_obj(cell)
        if not val or j == 0:
            continue
        if j == 1:
            result.append({'name': val, 'children': []})
        elif j == 2:
            parent = result[result.__len__() - 1]
            parent['children'].append({'name': val, 'children': []})
        else:
            parent = result[result.__len__() - 1]
            parentSub = parent['children']
            parentSub[parentSub.__len__() - 1]['children'].append({'name': val})

id_generator = 0


def build_row(r, p_id=0, seq=''):
    global id_generator
    id_generator += 1
    if not seq:
        seq = id_generator
    else:
        seq = '%s-%s' % (seq, id_generator)
    return id_generator, {'name': r['name'], 'id': id_generator, 'parent': p_id, 'seq': seq}


values_rows = []
for row in result:
    current_id, values_row = build_row(row)
    row['id'] = current_id
    values_rows.append(values_row)
    # values_row.append('(%s, %s, \'%s\', \'%s\', \'%s\', 1)' % (id_generator, 0, name, name, id_generator))

for row in result:
    parent_id = row['id']
    children = row['children']
    for c in children:
        current_id, values_row = build_row(c, parent_id, parent_id)
        c['id'] = current_id
        values_rows.append(values_row)

for row in result:
    parent_id = row['id']
    children = row['children']
    for cr in children:
        sub_parent_id = cr['id']
        sub_children = cr['children']
        for sc in sub_children:
            current_id, values_row = build_row(sc, sub_parent_id, '%s-%s' % (parent_id, sub_parent_id))
            sc['id'] = current_id
            values_rows.append(values_row)

sql_params = []
for vr in values_rows:
    sql_params.append(
        '(%s, %s, \'%s\', \'%s\', \'%s\', 1)' % (vr['id'], vr['parent'], vr['name'], vr['name'], vr['seq']))

sql = 'insert into component_classify (id, parent_id, name, code, classify_seq, status) ' \
      'values %s '

print(sql % ',\n'.join(sql_params))
