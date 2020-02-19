# -*- coding: utf-8 -*-


ROW_SYNTAX_NORMAL = 'normal'
ROW_SYNTAX_CASE = 'case'
ROW_SYNTAX_CASE_BETWEEN = 'case_between'
ROW_SYNTAX_COMPUTE = 'compute'

ROW_DTYPE_VARCHAR = 'VARCHAR'
ROW_DTYPE_INTEGER = 'INTEGER'

CASE_RELATION_EQUAL = '='
CASE_RELATION_EQUAL_NOT = '!='
CASE_RELATION_LESS = '<'
CASE_RELATION_LESS_EQ = '<='
CASE_RELATION_GREATER = '>'
CASE_RELATION_GREATER_EQ = '>='
CASE_RELATION_IN = 'in'
CASE_RELATION_NOT_IN = 'not in'
CASE_RELATION_NULL = 'is null'
CASE_RELATION_NOT_NULL = 'is not null'

CASE_RELATION_LIST = [
    CASE_RELATION_EQUAL,
    CASE_RELATION_EQUAL_NOT,
    CASE_RELATION_LESS,
    CASE_RELATION_LESS_EQ,
    CASE_RELATION_GREATER,
    CASE_RELATION_GREATER_EQ,
    CASE_RELATION_IN,
    CASE_RELATION_NOT_IN,
    CASE_RELATION_NULL,
    CASE_RELATION_NOT_NULL
]

CASE_RELATION_DICT = {
    "eq": CASE_RELATION_EQUAL,
    "eq_not": CASE_RELATION_EQUAL_NOT,
    "lt": CASE_RELATION_LESS,
    "lt_eq": CASE_RELATION_LESS_EQ,
    "gt": CASE_RELATION_GREATER,
    "gt_eq": CASE_RELATION_GREATER_EQ,
    "in": CASE_RELATION_IN,
    "not_in": CASE_RELATION_NOT_IN,
    "null": CASE_RELATION_NULL,
    "not_null": CASE_RELATION_NOT_NULL
}


class Row(object):
    __slots__ = 'name', 'alias', 'table', 'syntax', 'dtype', 'cases', 'compute', 'sql'

    def __init__(self, name='', alias='', table='', cases=list(), compute='', dtype=ROW_DTYPE_VARCHAR,
                 syntax=ROW_SYNTAX_NORMAL):
        self.name = name
        self.table = table
        self.dtype = dtype
        self.cases = cases
        self.compute = compute
        self.syntax = syntax
        self.alias = alias if alias != '' else '%s_%s' % (table, name)
        self.sql = self.__sql__()

    def __sql__(self):
        sql = ''
        if self.syntax == ROW_SYNTAX_NORMAL:
            sql = "%s.`%s` as '%s'" % (self.table, self.name, self.alias)
        elif self.syntax == ROW_SYNTAX_CASE:
            cs_str = ''
            for cs in self.cases:
                cs_ = ''
                if self.dtype == ROW_DTYPE_VARCHAR:
                    cs_ = "WHEN '%s' THEN '%s' " % (cs.get('key'), cs.get('val'))
                elif self.dtype == ROW_DTYPE_INTEGER:
                    cs_ = "WHEN %s THEN '%s' " % (cs.get('key'), cs.get('val'))
                cs_str = cs_str.__add__(cs_)
            sql = "case %s.`%s` %s end '%s'" % (self.table, self.name, cs_str, self.alias)
        elif self.syntax == ROW_SYNTAX_CASE_BETWEEN:
            cs_str = ''
            for cs in self.cases:
                cs_ = "WHEN %s.`%s` %s THEN '%s' " % (self.table, self.name, cs.get('key'), cs.get('val'))
                cs_str = cs_str.__add__(cs_)
            sql = "case %s end '%s'" % (cs_str, self.alias)
        elif self.syntax == ROW_SYNTAX_COMPUTE:
            sql = "%s.`%s`%s as '%s'" % (self.table, self.name, self.compute, self.alias)
        return sql

    def __str__(self):
        return self.sql


class Table(object):
    __slots__ = 'name', 'alias', 'sql'

    def __init__(self, name, alias):
        self.name = name
        self.alias = alias if alias != '' else name
        self.sql = self.__sql__()

    def __sql__(self):
        return '`%s` %s' % (self.name, self.alias)

    def __str__(self):
        return self.sql


class Join(object):
    __slots__ = 'jtype', 'table', 'on', 'sql'

    def __init__(self, table, jtype='join', on=list()):
        self.table = table
        self.jtype = jtype
        self.on = on
        self.sql = self.__sql__()

    def __sql__(self):
        cases = []
        for cs in self.on:
            if isinstance(cs, Case):
                cases.append(cs.sql)
        cases_ = 'and'.join(cases)
        return '%s `%s` %s on %s' % (self.jtype, self.table.name, self.table.alias, cases_)

    def __str__(self):
        return self.sql


class Case(object):
    __slots__ = 'relation', 'table', 'name', 'value', 'default', 'sql'

    def __init__(self, table, name, value, relation='=', default="''"):
        self.relation = self.__rel__(relation)
        self.table = table
        self.name = name
        self.default = default
        self.value = value if value is not None else default
        self.sql = self.__sql__()

    def __rel__(self, key_):
        if CASE_RELATION_LIST.__contains__(key_):
            return key_
        else:
            return CASE_RELATION_DICT[key_]

    def __sql__(self):
        if isinstance(self.value, Row):
            sql = ' %s.`%s` %s %s.`%s` ' % (self.table, self.name, self.relation, self.value.table, self.value.name)
        elif isinstance(self.value, list):
            val_str = tuple(self.value).__str__()
            sql = ' %s.`%s` %s %s ' % (self.table, self.name, self.relation, val_str)
        elif isinstance(self.value, int):
            sql = ' %s.`%s` %s %s ' % (self.table, self.name, self.relation, self.value)
        else:
            if self.relation == CASE_RELATION_NULL or self.relation == CASE_RELATION_NOT_NULL:
                sql = " %s.`%s` %s " % (self.table, self.name, self.relation)
            else:
                sql = " %s.`%s` %s '%s' " % (self.table, self.name, self.relation, self.value)
        return sql

    def __str__(self):
        return self.sql


class GroupBy(object):
    __slots__ = 'row', 'having', 'sql'

    def __init__(self, row, having=''):
        self.row = row
        self.having = having
        self.sql = self.__sql__()

    def __sql__(self):
        sql = ''
        if isinstance(self.row, list):
            sql_ = list()
            for r in self.row:
                str = r.get('str')
                if str is not None and str != '':
                    sql_.append(str)
                else:
                    row = Row(table=r.get('table'), name=r.get('name'))
                    sql_.append('%s.`%s`' % (row.table, row.name))
            sql = ', '.join(sql_)
        return sql

    def __str__(self):
        return self.sql


class OrderBy(object):
    __slots__ = 'row', 'otype', 'sql'

    def __init__(self, row, otype='DESC'):
        self.row = row
        self.otype = otype
        self.sql = self.__sql__()

    def __sql__(self):
        sql = ''
        if isinstance(self.row, Row):
            sql = '%s.`%s` %s' % (self.row.table, self.row.name, self.otype)
        return sql

    def __str__(self):
        return self.sql


if __name__ == '__main__':
    case = [{"key": 1, "val": "normal"}, {"key": 2, "val": "case"}]
    s = Row(name='phone', table='o', cases=case, dtype=ROW_DTYPE_INTEGER, syntax=ROW_SYNTAX_CASE)
    ss = Table(name='sb_user', alias='u')
    # print ss
    ro = ['1', '2', '3', '4', '5']
    cs = Case(name='user_id', table='o', relation='=', value=1)
    jo = Join(table=ss, on=[cs, cs])
    item = OrderBy(row=s)
    its = [item, item]
    r = [{
        "name": "id",
        "table": "o",
        "str": "o.id"
    }]
    gr = GroupBy(row=r)
