from torm.builder.BaseBuilder import BaseBuilder
from pymysql.cursors import DictCursor

from torm.utl.Expression import expression as expr, Expression
from combomethod import combomethod


import inspect

from torm.utl.Map import Map


def get_var_name(var, _depth=3):
    # 当前命名空间
    fr = inspect.currentframe()
    for i in range(_depth):
        fr = fr.f_back  # f_back获取父空间
    vars = fr.f_locals.items()  # 获取该命名空间的所有变量
    for var_name, var_val in vars:
        if var_val is var:  # 如果该变量的和var相同，则var_name就是var的变量名
            return var_name
    return None


def parse_args(args, kwargs, _depth=3):
    where = {}

    for arg in args:
        if type(arg) in [dict, set, Map]:
            arg = Map(arg, _depth=_depth)
            where.update(arg)
        elif type(arg) == str:
            key = get_var_name(arg, _depth=_depth)
            where[key] = arg

    where.update(kwargs)
    return where


class MysqlBuilder(BaseBuilder):
    operators = [
        '=', '<', '>', '<=', '>=', '<>', '!=',
        'like', 'like binary', 'not like', 'between', 'ilike',
        '&', '|', '^', '<<', '>>',
        'rlike', 'regexp', 'not regexp',
        '~', '~*', '!~', '!~*', 'similar to',
        'not similar to', 'not ilike', '~~*', '!~~*', 'in', 'not in', 'not between'
    ]

    __select__ = []                            # 检索的字段
    __where__ = []
    __orwhere__ = []                           # orwhere处理逻辑
    __whereor__ = []                           # orwhere处理逻辑

    __offset__ = None                          # offset
    __limit__ = None                           # 检索的数据条数
    __orderby__ = []                           # 排序字段
    __groupby__ = []  # 排序字段

    __lock__ = None                            # lock
    __join__ = []                              # leftjoin
    __union__ = []                             # union & unionall
    __on__ = []                                # leftjoin

    __having__ = None                          # having
    __subquery__ = []                          # subquery

    def __init__(self, *args, **kwargs):
        super().__init__()

    @combomethod
    def reset(self):
        self.__select__ = []
        self.__where__ = []
        self.__orwhere__ = []
        self.__whereor__ = []

        self.__offset__ = None
        self.__limit__ = None
        self.__orderby__ = []
        self.__groupby__ = []

        self.__lock__ = None
        self.__join__ = []
        self.__union__ = []
        self.__on__ = []

        self.__having__ = None
        self.__subquery__ = []

    # 增

    def create(self):
        data = self.to_dict()

        # 如果数据库是mysql，默认id无效
        if 'id' in data:
            data.pop('id')

        if data:
            if data and isinstance(data, dict):
                data = [
                    {key: value for key, value in data.items() if key in self.__field__}]

            sql = self._compile_create(data)
            self.connection.execute(sql)
        return self.lastid()

    def insert(self, columns, data):
        self.connection.execute(self._compile_insert(columns, data))
        return self

    @combomethod
    def create_table(self):
        charset = self.config['charset']
        key = "id"

        field_sql = ""
        for k in self.__field__:
            v = self.__fields__[k]
            if v.__class__.__name__ == 'Str':
                field_sql += f"`{v.name}` {v.field_type},"
            else:
                field_sql += f"`{v.name}` {v.field_type} NOT NULL DEFAULT {v.default},"

        sql = f"CREATE TABLE `{self.table_name}` ( {field_sql} PRIMARY KEY (`{key}`) ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT TORM_CHARSET={charset}; "
        self.connection.execute(sql)
        return None

    # 删
    def delete(self):
        return self.connection.execute(self._compile_delete())

    # 改
    def update(self, data):
        if data and isinstance(data, dict):
            #data = self._set_update_time(data)
            data = {key: value for key,
                    value in data.items() if key in self.__field__}
            return self.connection.execute(self._compile_update(data))

    @combomethod
    def first(self):
        self.__limit__ = 1
        data = self.get()
        if data:
            return data.pop()
        return data

    # 查
    @combomethod
    def get(self):
        sql = self._compile_select()
        try:
            result = self.connection.execute(sql, DictCursor)
        except Exception as e:
            print(sql)
            raise e
        return [Map(index) for index in result]

    @combomethod
    def all(self):
        sql = self._compile_select()
        try:
            result = self.connection.execute(sql, DictCursor)
        except Exception as e:
            print(sql)
            raise e
        return [Map(index) for index in result]

    # 计数
    @combomethod
    def count(self):
        self.__select__ = ['count(*) as aggregate']
        data = self.first()
        return data['aggregate'] if data else None

    # 聚合
    @combomethod
    def groupby(self, *args):
        self.__groupby__ = self._format_columns(list(args))
        return self

    # 常见sql操作
    @combomethod
    def select(self, *args):
        self.__select__ = self._format_columns(list(args))
        return self

    @combomethod
    def where(self, *args):
        length = args.__len__()
        if length == 1 and isinstance(args[0], dict):
            if args[0]:
                self.__where__.append(args[0])
        elif length == 2:
            self.__where__.append(
                {args[0]: self._check_columns_value(args[1])})
        elif length == 3:
            if args[1] in self.operators:
                if args[1] == '=':
                    self.__where__.append(
                        {args[0]: self._check_columns_value(args[2])})
                else:
                    self.__where__.append(
                        (args[0], args[1], self._check_columns_value(args[2])))
            else:
                raise Exception(
                    'operator key world not found: "{}"'.format(args[1]))
        else:
            raise Exception('bad parameters in where function')
        return self

    def lastid(self):
        data = self.connection.execute(self._compile_lastid())
        return data[0][0] if data and data[0] and data[0][0] else None

    def _compile_lastid(self):
        return 'select last_insert_id() as lastid'

    @combomethod
    def orderby(self, column, direction='asc'):
        if direction.lower() == 'asc':
            self.__orderby__.append(expr.format_column(column, self))
        else:
            self.__orderby__.append(expr.format_column(
                column, self.__model__) + ' desc')
        return self

    @combomethod
    def offset(self, number):
        if number < 0:
            raise Exception('offset number invalid')
        self.__offset__ = int(number)
        return self

    @combomethod
    def limit(self, number):
        if number <= 0:
            raise Exception('take number invalid')
        self.__limit__ = int(number)
        return self

    @combomethod
    def _columnize(self, columns):
        return tuple(columns).__str__().replace('\'', '`')

    @combomethod
    def _valueize(self, data):
        # return ','.join([tuple(index.values()).__str__() for index in data])
        return ','.join([str(tuple(index.values())).replace("'NULL'", 'null') for index in data])

    @combomethod
    def _format_columns(self, columns):
        return [expr.format_column(column, self) for column in columns]

    @combomethod
    def _check_columns_value(self, value):
        if self.__subquery__ and len(self.__subquery__) >= 2 and isinstance(value, str):
            tmp = value.split('.')
            if len(tmp) == 2 and tmp[0] in self._get_subquery_alias():
                return Expression(value)
        return value

    @combomethod
    def _compile_create(self, data):
        return "insert into {} {} values {}".format(self.table_name, self._columnize(data[0]), self._valueize(data))

    @combomethod
    def _compile_select(self):

        if len(self.__select__) == 0:
            self.__select__.append('*')

        sub_sql = ''.join(
            [self._compile_where(), self._compile_whereor(), self._compile_orwhere(), self._compile_groupby(), self._compile_orderby(),
             self._compile_having(), self._compile_limit(), self._compile_offset(), self._compile_lock()])

        join_sql = ''.join(self._compile_leftjoin())

        union_sql = ''.join(self._compile_union())

        return_sql = "select {} from {}{}{}".format(
            ','.join(self.__select__), self.table_name, join_sql, sub_sql, union_sql)

        return return_sql

    @combomethod
    def _compile_where(self):
        if len(self.__where__) > 0:
            sqlstr = []
            for index in self.__where__:
                if isinstance(index, dict):
                    sqlstr.append(' and '.join(self._compile_dict(index)))
                elif isinstance(index, tuple):
                    sqlstr.append(self._compile_tuple(index))
            return ' where {}'.format(' and '.join(sqlstr))
        return ''

    @combomethod
    def _compile_orwhere(self):
        if len(self.__orwhere__) > 0:
            sqlstr = []
            for index in self.__orwhere__:
                if isinstance(index, dict):
                    subsql = self._compile_dict(index)
                    if len(subsql) == 1:
                        sqlstr.append(subsql.pop())
                    else:
                        sqlstr.append('({})'.format(' and '.join(subsql)))
                elif isinstance(index, tuple):
                    sqlstr.append(self._compile_tuple(index))
                elif isinstance(index, list):
                    subsql = []
                    for items in index:
                        if len(items) == 2:
                            subsql.append(
                                self._compile_keyvalue(items[0], items[1]))
                        if len(items) == 3:
                            subsql.append(self._compile_tuple(
                                (items[0], items[1], items[2])))
                    sqlstr.append('({})'.format(' and '.join(subsql)))
                else:
                    raise Exception(
                        'undefined query condition {}'.format(index.__str__()))
            if len(self.__where__) > 0:
                return ' or {}'.format(' or '.join(sqlstr))
            return ' where {}'.format(' or '.join(sqlstr))
        return ''

    @combomethod
    def _compile_whereor(self):
        if len(self.__whereor__) > 0:
            sqlstr = []
            for index in self.__whereor__:
                subsql = []
                for item in index:
                    if isinstance(item, dict):
                        if len(item) == 1:
                            subsql.append(self._compile_dict(item).pop())
                        else:
                            subsql.append(
                                '(' + ' and '.join(self._compile_dict(item)) + ')')
                    elif isinstance(item, list):
                        if isinstance(item[0], str):
                            subsql.append(self._compile_tuple(tuple(item)))
                        else:
                            subsql.append(self._compile_lists(item))
                    elif isinstance(item, tuple):
                        subsql.append(self._compile_tuple(item))
                    else:
                        raise Exception('whereor param invalid')
                sqlstr.append(' or '.join(subsql))
            if len(self.__where__) > 0:
                return ' and ({})'.format(' or '.join(sqlstr))
            return ' where ({})'.format(' or '.join(sqlstr))
        return ''

    @combomethod
    def _compile_groupby(self):
        return '' if len(self.__groupby__) == 0 else ' group by ' + ','.join(self.__groupby__)

    @combomethod
    def _compile_orderby(self):
        return '' if len(self.__orderby__) == 0 else ' order by ' + ','.join(self.__orderby__)

    @combomethod
    def _compile_limit(self):
        return '' if self.__limit__ is None else ' limit {}'.format(self.__limit__)

    @combomethod
    def _compile_offset(self):
        return '' if self.__offset__ is None else ' offset {}'.format(self.__offset__)

    @combomethod
    def _compile_having(self):
        if self.__having__:
            return self.__having__
        return ''

    @combomethod
    def _compile_lock(self):
        return '' if self.__lock__ is None else self.__lock__

    @combomethod
    def _compile_leftjoin(self):
        if self.__join__:
            return ' ' + ' '.join(['{} {} on {}'.format(index, value._tablename(), value._compile_on()) for (index, value) in
                                   self.__join__])
        return ''

    @combomethod
    def _compile_union(self):
        if self.__union__:
            return ' ' + ' '.join(['{} ({})'.format(index, value.tosql()) for (index, value) in self.__union__])
        return ''

    @combomethod
    def _compile_dict(self, data):

        return ['{}={}'.format(expr.format_column(index, self), expr.format_string(value)) for index, value in data.items()]

    @combomethod
    def _compile_tuple(self, data):
        if data[1] in ['in', 'not in']:
            return self._compile_in((data[0], data[1], data[2]))
        elif data[1] in ['between', 'not between']:
            return self._compile_between((data[0], data[1], data[2]))
        return '{} {} {}'.format(expr.format_column(data[0], self), data[1], expr.format_string(data[2]))

    @combomethod
    def _compile_update(self, data):
        return "update {} set {}{}".format(self.table_name, ','.join(self._compile_dict(data)), self._compile_where())

    @combomethod
    def _compile_delete(self):
        return 'delete from {}{}'.format(self.table_name, self._compile_where())

    @combomethod
    def InsertOne(self, item):
        self.reset()
        self.validate_type(item)
        item = self(item)
        return item.create()

    @combomethod
    def InsertMany(self, items):
        self.reset()
        all_validate_type = all([self.validate_type(item) for item in items])
        if not all_validate_type:
            raise TypeError(f'all list element must be {self.__class__} type')

        result = []
        for item in items:
            item = self(item)
            result.append(item.create())
        return result

    @combomethod
    def FindOne(self, *args, **kwargs):
        self.reset()
        where = parse_args(args, kwargs, _depth=4)
        items = self.where(where).limit(1).get()
        if not items:
            return None
        item = Map(items[0])
        return item

    @combomethod
    def FindMany(self, *args, **kwargs):
        self.reset()
        where = parse_args(args, kwargs, _depth=4)
        items = self.where(where).get()
        if not items:
            return None
        items = [Map(item) for item in items]
        return items

    @combomethod
    def UpdateOne(self, where={}, item={}):
        self.reset()
        if not where:
            return None
        if not item:
            return None
        where = Map(where, _depth=4)

        if not isinstance(item, self.__class__):
            item = self.__class__(item)

        item = item.to_dict()
        # 禁止更新id字段
        if "id" in item:
            item.pop("id")

        # 先查找第一个，然后更新
        _item = self.FindOne(where)
        if _item:
            return self.where({'id': _item.id}).update(item)
        else:
            return None

    @combomethod
    def DeleteOne(self, *args, **kwargs):
        self.reset()
        where = parse_args(args, kwargs, _depth=4)
        _item = self.FindOne(where)
        if _item:
            return self.where({'id': _item.id}).delete()
        else:
            return None
