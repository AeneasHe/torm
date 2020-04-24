import collections

from torm.utl.Config import config
from torm.field import *
from torm.builder import MongoBuilder, MysqlBuilder
from torm.connection import MongoConnection, MysqlConnection


def _connection(config):
    if config['db_type'] == 'mongo':
        return MongoConnection(config)


class ModelMetaclass(type):
    isinstance = False
    isclass = True

    @classmethod
    def __prepare__(cls, name, bases, **kws):
        return collections.OrderedDict()

    # 返回子类
    def __new__(cls, name, bases, attrs):

        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)  # 返回Model类型

        fields = dict()
        keys = list(attrs.keys())
        for k in keys:
            if isinstance(attrs[k], Field):
                fields[k] = attrs[k]
#                attrs.pop(k)

        field = fields.keys()
        attrs['__fields__'] = fields  # 保存字段的属性
        attrs['__field__'] = list(field)  # 保存字段名列表
        attrs['__config__'] = cls.init_config(cls, name, attrs)

        attrs['config'] = attrs['__config__']
        attrs['connection'] = _connection(attrs['__config__'])
        attrs['db_name'] = attrs['__config__']['db']
        attrs['table_name'] = attrs['__config__']['table']

        # 根据数据库类型，继承各数据库的builder
        dbtype = attrs['__config__']['db_type']
        if dbtype == 'mongo':
            bases = bases + (MongoBuilder,)
        elif dbtype == 'mysql':
            bases = bases + (MysqlBuilder,)

        return type.__new__(cls, name, bases, attrs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init_config(cls, name, attrs):
        __config = {}
        # 环境变量配置名称
        env_name = attrs.get("__config__", "default")

        db_type = attrs.get(
            "__dbtype__", config.env(env_name)('DBTYPE'))

        # 配置名称
        __config['config_name'] = env_name
        # 数据库类型
        __config['db_type'] = db_type
        # 数据库名
        __config['db'] = attrs.get("__db__", config.env(env_name)('DB'))
        # 表名
        __config['table'] = attrs.get("__table__", name.lower())

        # 连接参数
        __config['host'] = config.env(env_name)('HOST')
        __config['port'] = int(config.env(env_name)('PORT'))
        __config['charset'] = config.env(env_name)('CHARSET')

        # 用户配置
        if db_type == "mysql":
            __config['user'] = config.env(env_name)('USER')
            __config['password'] = config.env(env_name)('PASSWORD')

        return __config

    def __getattribute__(self, key):
        if key == "__new__":
            return object.__new__(self)
        try:
            return object.__getattribute__(self, key)
        except:
            return getattr(object.__new__(self), key)
