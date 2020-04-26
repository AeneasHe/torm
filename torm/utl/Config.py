from configparser import ConfigParser

import os

from environs import Env


class Config(object):
    __instance = None

    # 单例模式
    def __new__(cls, *args, **kws):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kws)
        return cls.__instance

    def __init__(self):
        env = Env()
        # env.read_env()
        self.__env = env

    def reset(self, name='default'):
        path = '.env' if name == 'default' else '.env.' + name
        env = Env()
        env.read_env(path=path, override=True)
        self.__env = env

    # 读取配置文件
    def env(self, name='default'):
        path = '.env' if name == 'default' else '.env.' + name
        env = Env()

        err = None
        try:
            env.read_env(path=path, override=True)
        except Exception as e:
            if name == 'default':
                os.environ["TORM_DB_TYPE"] = "mongo"
                os.environ["TORM_DB"] = "test"
                os.environ["TORM_HOST"] = "127.0.0.1"
                os.environ["TORM_PORT"] = "27017"
                os.environ["TORM_CHARSET"] = "utf8mb4"
                env = Env()
            elif str(e) == 'Starting path not found':
                err = Exception(
                    f"env file '{path}' for config name '{name}' not found.")
            else:
                raise(e)
        if err:
            raise err

        return env

    def __getattr__(self, name):
        return self.__env(name)


config = Config()
