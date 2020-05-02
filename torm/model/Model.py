import pandas as pd
import time

from torm.model.ModelMetaclass import *
from collections import OrderedDict
from combomethod import combomethod
from torm.utl.Map import Map


class Model(metaclass=ModelMetaclass):
    def __init__(self, *args, **kws):
        # 实例化的参数
        attrs = {}
        if args:
            if args[0] == None:
                pass
            elif isinstance(args[0], dict):
                attrs = dict(args[0])
            else:
                attrs = dict(zip(self.__field__, args))
        attrs.update(kws)

        # 将属性绑定到Model上,只绑定field的属性，多余的丢弃
        # print(self.config['db_type'])  # 数据库类型
        db_type = self.config['db_type']

        for key in self.__field__:
            # 检查数据库是否支持该字段的类型
            if self.__fields__[key].only_db_types:
                if not self.config['db_type'] in self.__fields__[key].only_db_types:
                    raise TypeError(
                        f'type of "{key}" {self.__fields__[key]} can only be used in db {self.__fields__[key].only_db_types}')

            if key in attrs:  # 如果对象的参数有该字段的值，就采用该值
                if attrs[key] == None:  # 如果该值为None,采用该字段的默认值
                    setattr(self, key, self.__fields__[key].default)
                else:
                    setattr(self, key, attrs[key])
            else:  # 没有提供该值，就采用默认值
                setattr(self, key, self.__fields__[key].default)

        # 父类Builder初始化
        super().__init__()
        self.isinstance = True
        self.isclass = False

    def __len__(self):
        return len(self.__field__)

    def __getattribute__(self, key):
        return object.__getattribute__(self, key)

    def __getattr__(self, key):
        raise AttributeError(r"%s has no attribute or method '%s'" % (
            self.__class__.__name__, key))

    def __setattr__(self, key, value):
        # 限制可以绑定的属性
        if key in self.__field__:
            object.__setattr__(self, key, value)
        elif key in ['connection', 'config', 'table_name', 'isinstance', 'isclass'] or (key.startswith('__') and key.endswith('__')):
            object.__setattr__(self, key, value)
        else:
            raise AttributeError(r"%s can not bind attribute '%s'" % (
                self.__class__.__name__, key))

    def __len__(self):
        return len(self.__field__)

    def __setitem__(self, key, value):
        if key in self.__field__:
            self.__setattr__(key, value)

    def __getitem__(self, key):
        if key in self.__field__:
            return self.__getattribute__(key)
        else:
            raise AttributeError(r"%s has no attribute '%s'" % (
                self.__class__.__name__, key))

    def __iter__(self):
        for key in self.__field__:
            yield key, self[key]

    def __str__(self, pretty=False):
        if not self.__bool__():
            return 'Null'
        values = ', '.join('{}={!r}'.format(
            i, self[i]) for i in self.__field__)
        return '{}({})'.format(self.__class__.__name__, values)

    def __bool__(self):
        # 如果所有字段都是空，则返回False,否则返回True
        bools = [bool(self[i]) for i in self.__field__]
        if True in bools:
            return True
        else:
            return False

    def __call__(self, *args, **kws):
        if len(args):
            if type(args[0]) == dict:
                kws.update(args[0])
        try:
            for k in self.__field__:
                v = kws.get(k)
                if v:
                    self.__setattr__(k, v)
            return self
        except Exception as e:
            return e

    def pretty(self):
        values = ', '.join('\n    {} = {!r}'.format(
            i, self[i]) for i in self.__field__)
        return '{}({}\n)'.format(self.__class__.__name__, values)

    def to_dict(self):
        d = dict()
        for i in self.__field__:
            d[i] = self[i]
        return d

    def to_ordict(self):
        d = OrderedDict()
        for i in self.__field__:
            d[i] = self[i]
        return d

    def to_map(self):
        return Map(self.to_ordict())

    @combomethod
    def to_df(self):
        return pd.DataFrame.from_records(self.get())

    def gets(self, id, name):
        print(id, name)
