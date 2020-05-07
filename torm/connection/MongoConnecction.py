
from .Connection import Connection
import pymongo
from urllib import parse


class MongoConnection(Connection):
    _instance = None
    _conn = None
    _config = None

    # 单例模式
    @classmethod
    def __new__(cls, *args, **kws):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config):
        super().__init__(config)
        self._config = config

    # 连接数据库
    def connect(self):
        config = self._config

        if 'user' and 'password' in config:
            user = parse.quote_plus(config['user'])
            password = parse.quote_plus(config['password'])
            MONGO_URL = f"mongodb://{user}:{password}@{config['host']}:{config['port']}/"
        else:
            MONGO_URL = f"mongodb://{config['host']}:{config['port']}/"
        conn = pymongo.MongoClient(MONGO_URL)

        return conn[config['db']]

    # 返回数据库
    def db(self, tablename):
        return self.connect()[tablename]

    def table(self, builder):
        tb = builder.table_name
        return self.db(tb)
    # 增

    def create(self, builder, data):
        tb = builder.table_name
        return self.db(tb).insert(data)

    # 删
    def delete(self, builder):
        return self.db(builder.table_name).delete_many(builder.__where__)

    # 改
    def update(self, builder, data, **kwargs):
        return self.db(builder.table_name).update_many(builder.__where__, data, **kwargs)

    # 查
    def get(self, builder):

        _select = builder.__select__ if builder.__select__ else {'_id': 0}

        tb = builder.table_name

        model = self.db(tb).find(builder.__where__, _select).skip(
            builder.__offset__).limit(builder.__limit__)

        return list(model)

    # 计数
    def count(self, builder):
        return self.db(builder.table_name).find(builder.__where__).count()

    # 聚合
    def groupby(self, builder):
        # 聚合操作的列表
        aggre = [builder.where_to_match(), builder.__groupby__]
        if builder.__orderby__.__len__() > 0:
            aggre.append(builder._compile_aggregate_orderby())
        if builder.__offset__ > 0:
            aggre.append(builder._compile_aggregate_offset())
        if builder.__limit__ > 0:
            aggre.append(builder._compile_aggregate_limit())
        aggre.append(builder._compile_aggregate_project())

        # mongo的聚合
        return self.db(builder.table_name).aggregate(aggre)
