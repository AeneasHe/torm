from .Connection import Connection
from .Pool.MysqlConnectionPool import connectionPool


class MysqlConnection(Connection):
    _connection = {}

    _instance = None
    # 单例模式

    @classmethod
    def __new__(cls, *args, **kws):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config):
        super().__init__(config)
        self._config = config

    def connect(self):
        db = self._config['db']

        if self._connection.get(db, None) is None:
            self._connection[db] = connectionPool.connection(self._config, db)
        return self._connection[db]

    def execute(self, sql, cursorclass=None):
        if cursorclass:
            cursor = self.connect().cursor(cursor=cursorclass)
        else:
            cursor = self.connect().cursor()
        error = None
        try:
            cursor.execute(sql)
        except Exception as e:
            e = str(e).strip("(").strip(")")
            error = Exception(e)
        if error:
            raise error

        data = cursor.fetchall()

        if not hasattr(self, '_transaction'):
            self.connect().commit()
        cursor.close()
        return data

    def transaction(self, callback):
        try:
            self.start()
            result = callback()
            self.connect().commit()
            self.end()
            return result
        except Exception as e:
            self.connect().rollback()
            self.end()
            raise e

    def transaction_wrapper(self, callback):
        @wraps(callback)
        def wrapper(*args, **kwargs):
            try:
                self.start()
                result = callback(*args, **kwargs)
                self.connect().commit()
                self.end()
                return result
            except Exception as e:
                self.connect().rollback()
                self.end()
                raise e

        return wrapper

    @classmethod
    def instance(cls, database, config):
        if cls._instance.get(database, None) is None:
            cls._instance[database] = MysqlConnection(database, config)
        return cls._instance.get(database, None)

    def start(self):
        self._transaction = True

    def end(self):
        del self._transaction

    def _sql_create_table(self):
        pass
