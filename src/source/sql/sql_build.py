# -*- coding: utf-8 -*-

import os
import json
import copy

from .sql_helper import *


def load_sql_file():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    all_db_file = os.path.join(os.path.join(base_dir, 'resource'), 'sql_config.json')
    with open(all_db_file, 'r+') as f:
        t = f.read()
        info = json.loads(t)

    return info


def transform_to_dict(sqls):
    sql_dict_ = dict()
    if isinstance(sqls, dict):
        for k, v in sqls.items():
            try:
                val_copy = copy.deepcopy(v)
                sql_dict[k] = transform_sql(sql=val_copy)
            except Exception as e:
                sql_dict[k] = ''
    return sql_dict_


def transform_sql(sql):
    rows_str = _transform_sql_rows(sql)
    table_str = _transform_sql_table(sql)
    join_str = _transform_sql_join(sql)
    case_str = _transform_sql_case(sql)
    group_str = _transform_sql_group(sql)
    order_str = _transform_sql_order(sql)
    return '%s %s %s %s %s %s' % \
           (rows_str, table_str, join_str, case_str, group_str, order_str)


def _transform_sql_rows(sql):
    rows = sql.get('rows')
    rows_ = []
    if isinstance(rows, list):
        for r in rows:
            rs = Row(**r)
            rows_.append(rs.__str__())

    row_str = ''
    if rows_.__len__() > 0:
        row_str = 'select \n%s' % (',\n'.join(rows_))
    return row_str


def _transform_sql_table(sql):
    table = sql.get('table')
    return '\n' 'from %s ' % Table(**table).__str__()


def _transform_sql_join(sql):
    joins = sql.get('join')
    joins_ = []
    if isinstance(joins, list):
        for join in joins:
            td = join.get('table')
            join['table'] = Table(**td)

            ons = join.get('on')
            ons_ = list()
            for on in ons:
                on_val = on.get('value')
                if isinstance(on_val, dict):
                    on['value'] = Row(**on_val)
                ons_.append(Case(**on))

            join['on'] = ons_
            joins_.append(Join(**join).__str__())
    joins_str = ''
    if joins_.__len__() > 0:
        joins_str = '\n'.__add__('\n'.join(joins_))
    return joins_str


def _transform_sql_case(sql):
    case = sql.get('case')
    case_ = list()

    if isinstance(case, list):
        for cs in case:
            cs_val = cs.get('value')
            if isinstance(cs_val, dict):
                cs['value'] = Row(**cs_val)
            case_.append(Case(**cs).__str__())

    case_str = ''
    if case_.__len__() > 0:
        case_str = '\n''where%s' % ('\nand'.join(case_))
    return case_str


def _transform_sql_group(sql):
    group = sql.get('group')
    group_str = ''
    if isinstance(group, dict):
        group_str = GroupBy(**group).__str__()

    if group_str != '':
        group_str = '\n''group by %s' % group_str
    return group_str


def _transform_sql_order(sql):
    orders = sql.get('order')
    orders_ = list()
    if isinstance(orders, list):
        for o in orders:
            row = Row(**o.get('row'))
            o['row'] = row
            orders_.append(OrderBy(**o).__str__())

    order_str = ''
    if orders_.__len__() > 0:
        order_str = '\n''order by %s' % (','.join(orders_))
    return order_str


def build_sql_with_params(key, params=list()):
    sql_ = ''
    key_json = sql_json.get(key)
    if isinstance(key_json, dict):
        key_json_ = copy.deepcopy(key_json)
        cases = key_json_.get('case')
        for ps in params:
            cases.append(ps)

        sql_ = transform_sql(key_json_)

    return sql_


sql_json = load_sql_file()
sql_dict = transform_to_dict(sql_json)

if __name__ == '__main__':
    l = [
        {
            "table": "sc",
            "name": "status",
            "relation": "eq_not",
            "value": 1
        },
        {
            "table": "su",
            "name": "status",
            "relation": "eq",
            "value": 1
        }
    ]
    print(sql_dict.get('ybb_school_order'))
    print(build_sql_with_params('ybb_user_order', l))
    print(build_sql_with_params('ybb_user_order'))
    print(build_sql_with_params('ybb_user_order'))
