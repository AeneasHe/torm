from torm.builder.BaseBuilder import BaseBuilder
from torm.utl.Map import Map

from bson.objectid import ObjectId

import pymongo
from combomethod import combomethod

import inspect


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


def decode_id(result):
    if not result:
        return result
    if "_id" in result:
        result["id"] = str(result["_id"])
        result.pop("_id")
    return result


def encode_id(arg):
    if "id" in arg:
        # 如果id是空的，就去除，由数据库生成id
        if str(arg["id"]):
            arg["_id"] = ObjectId(str(arg["id"]))
        arg.pop("id")
    return arg


def parse_args(args, kwargs, _depth=3):
    where = {}

    for arg in args:
        if type(arg) in [dict, set]:
            arg = Map(arg, _depth=_depth)
            arg = encode_id(arg)
            where.update(arg)
        elif type(arg) == str:
            key = get_var_name(arg, _depth=_depth)
            if key == "id":
                where["_id"] = ObjectId(str(arg))
            else:
                where[key] = arg

    kwargs = encode_id(kwargs)

    where.update(kwargs)
    return where


class MongoBuilder(BaseBuilder):
    operators = [
        '=', '<', '>', '<=', '>=', '<>', '!=',
        'like', 'in', 'not in', 'not between', 'exist',
        'not like', 'ilike', 'not ilike', 'between', 'mod', 'all', 'size'
    ]
    operators_map = {
        '<': '$lt',
        '<=': '$lte',
        '>': '$gt',
        '>=': '$gte',
        '!=': '$ne',
        'in': '$in',
        'not in': '$nin',
        'like': '$regex',
        'ilike': '$regex',
        'not like': '$regex',
        'not ilike': '$regex',
        'exist': '$exists',
        'mod': '$mod',
        'all': '$all',
        'size': '$size',
    }
    __select__ = {}     # 检出的字段
    __where__ = {}      # 刷选
    __offset__ = 0      # offset
    __limit__ = 0    # 检索的数据条数
    __orderby__ = []    # 排序字段
    __groupby__ = []    # 排序字段
    __lock__ = None     # lock
    __join__ = []       # leftjoin
    __union__ = []      # union & unionall
    __on__ = []         # leftjoin
    __having__ = None       # having
    __subquery__ = []       # subquery
    __groupbykey__ = None   # mongo groupby 字段名

    def __init__(self, *args, **kwargs):
        super().__init__()

    @combomethod
    def reset(self):
        self.__select__ = {}
        self.__where__ = {}
        self.__offset__ = 0
        self.__limit__ = 0
        self.__orderby__ = []
        self.__groupby__ = []

        self.__lock__ = None
        self.__join__ = []
        self.__union__ = []
        self.__on__ = []

        self.__having__ = None
        self.__subquery__ = []
        self.__groupbykey__ = None

    # 增

    def create(self):
        data = self.to_ordict()
        if data:
            if isinstance(data, dict):
                data = [data]
            # data = self._set_create_time(data)
                return str(self.connection.create(self, data))
        return None

    # 删

    def delete(self):
        # if self.isinstance:
        #     self.__where__.update(self.dict())
        r = self.connection.delete(self)
        # self.reset()
        return r

    # 改

    @combomethod
    def update(self, data, **kwargs):
        r = None
        if data and isinstance(data, dict):
            # data = self._set_update_time(data)
            r = self.connection.update(self, {'$set': data}, **kwargs)
        self.reset()
        return r

    # 查

    @combomethod
    def first(self):
        self.__limit__ = 1
        data = self.get()
        if data:
            return data.pop()

        self.reset()
        return data

    @combomethod
    def get(self):
        d = self.connection.get(self)
        self.reset()
        return [Map(index) for index in d]

    # 计数

    @combomethod
    def count(self):
        return self.connection.count(self)

    # 聚合
    @combomethod
    def groupby(self, groupkey):
        groupby = {
            "$group": {}
        }
        if self.__select__.__len__() == 0:
            raise Exception('invalid select filed')
        for key, value in self.__select__.items():
            if value == 1:
                groupby['$group'].update(self.format_group_sql(key))
        self.__select__ = {}
        self.__groupby__ = groupby
        self.__groupbykey__ = groupkey
        return self

    # 常见sql操作
    @combomethod
    def select(self, *args):
        self.__select__.update({'_id': 0})
        [self.__select__.update({index: 1}) for index in args]
        return self

    @combomethod
    def where(self, *args, **kwargs):
        length = args.__len__()
        if length == 0:
            where = parse_args(args, kwargs)
            self.__where__.update(where)
        elif length == 1 and isinstance(args[0], dict):
            if args[0]:
                where = parse_args(args, kwargs)
                self.__where__.update(where)

        elif length == 2:
            if self.__where__.get('$and', None) is None:
                self.__where__['$and'] = []
            where = parse_args((), {args[0]: args[1]})
            self.__where__['$and'].append(where)

        elif length == 3:
            if self.__where__.get('$and', None) is None:
                self.__where__['$and'] = []
            if args[1] in self.operators:
                if args[1] == '=':
                    where = parse_args((), {args[0]: args[2]})
                    self.__where__['$and'].append(where)
                else:
                    where = self._compile_tuple((args[0], args[1], args[2]))
                    where = parse_args((), where)
                    self.__where__['$and'].append(where)
            else:
                raise Exception(
                    'operator key world not found: "{}"'.format(args[1]))
        else:
            raise Exception('bad parameters in where function')

        return self

    # @combomethod
    # def _check_columns_value(self, value):
    #     if self.__subquery__ and len(self.__subquery__) >= 2 and isinstance(value, str):
    #         tmp = value.split('.')
    #         if len(tmp) == 2 and tmp[0] in self._get_subquery_alias():
    #             return Expression(value)
    #     return value

    @combomethod
    def orderby(self, column, direction='asc'):
        if direction.lower() == 'asc':
            self.__orderby__.append((column, pymongo.ASCENDING))
        else:
            self.__orderby__.append((column, pymongo.DESCENDING))
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
            raise Exception('limit number invalid')
        self.__limit__ = int(number)
        return self

    # 执行事物
    @combomethod
    def execute(self, sql):
        return self.connection.execute(sql)
    # 将操作编译成字典

    def _compile_tuple(self, data):
        # data=('time', 'between', ['14:08:38', '14:11:37'])
        # 对应：字段，操作符，操作参数

        if data[1] == 'not like':
            return {data[0]: {self.operators_map[data[1]]: '^((?!{}).)*$'.format(data[2])}}
        elif data[1] == 'ilike':
            return {data[0]: {self.operators_map[data[1]]: data[2], '$options': 'i'}}
        elif data[1] == 'not ilike':
            return {data[0]: {self.operators_map[data[1]]: '^((?!{}).)*$'.format(data[2]), '$options': 'i'}}
        elif data[1] == 'between':
            if len(data[2]) != 2:
                raise Exception('between param error')
            return {data[0]: {'$lte': data[2][1], '$gte': data[2][0]}}
        elif data[1] == 'not between':
            if len(data[2]) != 2:
                raise Exception('not between param error')
            return {'$or': [{data[0]: {'$gt': data[2][1]}}, {data[0]: {'$lt': data[2][0]}}]}
        else:
            return {data[0]: {self.operators_map[data[1]]: data[2]}}

    @combomethod
    def InsertOne(self, item):
        self.validate_type(item)
        item = encode_id(dict(item))
        table = self.connection.table(self)
        r = table.insert_one(item)
        if r:
            return str(r.inserted_id)
        return None

    @combomethod
    def InsertMany(self, items):
        all_validate_type = all([self.validate_type(item) for item in items])
        if not all_validate_type:
            raise TypeError(f'all list element must be {self.__class__} type')

        table = self.connection.table(self)
        items = [encode_id(item.to_ordict()) for item in items]
        return table.insert_many(items)

    @combomethod
    def FindOne(self, *args, **kwargs):
        where = parse_args(args, kwargs, _depth=4)

        table = self.connection.table(self)

        item = table.find_one(where)
        if not item:
            return None

        # 将字典转成Model
        item = Map(decode_id(item))
        return item

    @combomethod
    def FindMany(self, *args, **kwargs):
        where = parse_args(args, kwargs)
        table = self.connection.table(self)
        items = table.find(where)
        if not items:
            return []
        items = [Map(decode_id(item)) for item in items]
        return items

    @combomethod
    def UpdateOne(self, where={}, item={}):

        if not where:
            return None
        where = Map(where, _depth=4)
        where = encode_id(where)

        if not item:
            return None

        if isinstance(item, self.__class__):
            item = item.to_dict()

        # 禁止更新id,_id字段
        if "id" in item:
            item.pop("id")
        if "_id" in item:
            item.pop("_id")

        table = self.connection.table(self)
        r = table.update_one(where, {"$set": item})
        return r

    @combomethod
    def DeleteOne(self, *args, **kwargs):
        where = parse_args(args, kwargs, _depth=4)
        table = self.connection.table(self)
        r = table.delete_one(where)
        return r
