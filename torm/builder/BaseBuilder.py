from torm.connection import MongoConnection, MysqlConnection
from combomethod import combomethod


def _connection(config):
    if config['db_type'] == 'mongo':
        return MongoConnection(config)

    if config['db_type'] == 'mysql':
        return MysqlConnection(config)

    if config['db_type'] == 'sqlite':
        return SqliteConnection(config)


class BaseBuilder():

    def __new__(cls, *args, **kws):
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        super().__init__()

    def _connection(self):
        config = self.__config__

        if config['db_type'] == 'mongo':
            return MongoConnection(config)

        if config['db_type'] == 'mysql':
            return MysqlConnection(config)

        if config['db_type'] == 'sqlite':
            return SqliteConnection(config)
