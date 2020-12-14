#!/usr/bin/python
# -*- coding: utf-8 -*-
from util.logger.logger import Logger
from source.orm.field import Field

logger = Logger(__name__)


class ModelMetaclass(type):
    def __new__(mcs, name, bases, attr):
        # 排除Model类本身:
        if name == 'Model':
            return type.__new__(mcs, name, bases, attr)
        # 获取table名称:
        table_name = attr.get('__table__', None) or name
        logger.info('found model: %s (table: %s)' % (name, table_name))
        # 获取所有的Field和主键名:
        mappings = dict()
        fields = []
        primary_key = None
        for k, v in attr.items():
            if isinstance(v, Field):
                logger.info('found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    # 找到主键:
                    if primary_key:
                        raise RuntimeError('Duplicate primary key for field: %s' % k)
                    primary_key = k
                else:
                    fields.append(k)
        if not primary_key:
            raise RuntimeError('Primary key not found.')
        for k in mappings.keys():
            attr.pop(k)
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))
        attr['__mappings__'] = mappings  # 保存属性和列的映射关系
        attr['__table__'] = table_name
        attr['__primary_key__'] = primary_key  # 主键属性名
        attr['__fields__'] = fields  # 除主键外的属性名
        # 构造默认的SELECT, INSERT, UPDATE和DELETE语句:
        attr['__select__'] = 'select `%s`, %s from `%s`' % (primary_key, ', '.join(escaped_fields), table_name)
        attr['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (
            table_name, ', '.join(escaped_fields), primary_key, create_args_string(len(escaped_fields) + 1))
        attr['__update__'] = 'update `%s` set %s where `%s`=?' % (
            table_name, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primary_key)
        attr['__delete__'] = 'delete from `%s` where `%s`= ?' % (table_name, primary_key)
        return type.__new__(mcs, name, bases, attr)


def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)
