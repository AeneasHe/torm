from torm.connection import MongoConnection, MysqlConnection
from combomethod import combomethod


def _connection(config):
    if config['db_type'] == 'mongo':
        return MongoConnection(config)

    if config['db_type'] == 'mysql':
        return MysqlConnection(config)


class BaseBuilder():

    def __new__(cls, *args, **kws):
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        super().__init__()

    @combomethod
    def validate_type(self, item):
        if isinstance(item, self.__class__):
            return True
        else:
            try:
                item = self(item)
            except Exception as e:
                raise TypeError(
                    f'item must be or change to {self.__class__} type')
            return True

    def _connection(self):
        config = self.__config__

        if config['db_type'] == 'mongo':
            return MongoConnection(config)

        if config['db_type'] == 'mysql':
            return MysqlConnection(config)
