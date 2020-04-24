from torm.connection.ConnectionMetaClass import *


class Connection(metaclass=ConnectionMetaclass):
    __config__ = ""

    def __init__(self, config):
        self.__config__ = config
        self.db_name = config['db']
