import collections
import urllib.parse

from torm.utl.Config import config
from torm.utl.Utl import to_snake_name
from torm.field import *
from torm.builder import MongoBuilder, MysqlBuilder
from torm.connection import MongoConnection, MysqlConnection


def _connection(config):
    if config['db_type'] == 'mongo':
        return MongoConnection(config)
    if config['db_type'] == 'mysql':
        return MysqlConnection(config)


class ModelMetaclass(type):
    isinstance = False
    isclass = True

    @classmethod
    def __prepare__(cls, name, bases, **kws):
        return collections.OrderedDict()

    # 返回子类
    def __new__(cls, name, bases, attrs):
        '''
        name:类名
        bases:父类
        attrs:类的所有属性字典
        '''
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)  # 返回Model类型

        model_fields = dict()

        cls_keys = list(attrs.keys())
        for k in cls_keys:
            if isinstance(attrs[k], Field):
                model_fields[k] = attrs[k]

        field = model_fields.keys()
        attrs['__fields__'] = model_fields  # 保存字段的属性
        attrs['__field__'] = list(field)  # 保存字段名列表
        attrs['__config__'] = cls.init_config(cls, name, attrs)  # 连接配置

        attrs['config'] = attrs['__config__']
        attrs['db_name'] = attrs['__config__']['db']

        # attrs['table_name'] = attrs['__config__']['table']
        # attrs['connection'] = _connection(attrs['__config__'])

        # 根据数据库类型，继承各数据库的builder
        dbtype = attrs['__config__']['db_type']
        bases = bases + (dict,)
        if dbtype == 'mongo':
            builder = MongoBuilder
        elif dbtype == 'mysql':
            builder = MysqlBuilder

        builder.__config__ = attrs['__config__']
        builder.table_name = attrs['__config__']['table']
        builder.connection = _connection(attrs['__config__'])

        attrs['builder'] = builder()
        # attrs['model']=

        # bases = bases + (builder,)
        # cls.builder = builder
        # 使Model同时继承builder
        return type.__new__(cls, name, bases, attrs)

    def __init__(self, *args, **kwargs):
        if self.__name__ != 'Model':
            self.builder.model = self
        super().__init__(*args, **kwargs)

    def init_config(cls, name, attrs):
        __config = {}
        # 环境变量配置名称
        env_name = attrs.get("__config__", "default")

        db_type = attrs.get(
            "__dbtype__", config.env(env_name)('TORM_DB_TYPE'))

        # 配置名称
        __config['config_name'] = env_name
        # 数据库类型
        __config['db_type'] = db_type

        # 表名
        __config['table'] = attrs.get(
            "__tablename__",
            to_snake_name(name)
        )

        if db_type == "mysql":
            __config['charset'] = config.env(env_name)('TORM_CHARSET')
            __config['host'] = config.env(env_name)('TORM_HOST')
            __config['port'] = int(config.env(env_name)('TORM_PORT'))
            __config['db'] = attrs.get(
                "__dbname__",
                config.env(env_name)('TORM_DB')
            )
        else:
            # 数据库连接参数
            __config['url'] = config.env(env_name)('TORM_URL', default=None)
            if not __config['url']:
                __config['host'] = config.env(env_name)('TORM_HOST')
                __config['port'] = int(config.env(env_name)('TORM_PORT'))
                __config['db'] = attrs.get(
                    "__dbname__",
                    config.env(env_name)('TORM_DB')
                )
            else:
                url_parts = urllib.parse.urlparse(__config['url'])
                path_parts = url_parts[2].rpartition('/')
                if path_parts[2]:
                    __config['db'] = attrs.get(
                        "__dbname__",
                        path_parts[2]
                    )
                else:
                    __config['db'] = attrs.get(
                        "__dbname__",
                        config.env(env_name)('TORM_DB')
                    )

        # 数据库用户名和密码配置
        auth = config.env(env_name)("TORM_AUTH", default="off")
        if auth == "on":
            __config['user'] = config.env(env_name)('TORM_USER')
            __config['password'] = config.env(env_name)('TORM_PASSWORD')

        return __config

    def __getattribute__(self, key):
        if key == "__new__":
            # return object.__new__(self)
            # print(self)
            return dict.__new__(self)
        try:
            return object.__getattribute__(self, key)
        except:

            return self.builder.__getattribute__(key)
