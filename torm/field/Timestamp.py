from torm.field import Field
from torm.utl.Error import *


class Timestamp(Field):

    def __init__(self, *args, **kws):

        default = {
            'left': None,
            'right': None,
            'meta': 'left',
            'default': 0,
            'field_type': 'int(16)',
            'key': False,
            'only_db_types': None
        }

        default.update(kws)

        super().__init__(**default)

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if self.validate(value):
            self.value = value

    def validate(self, value):
        model = self.model
        key = self.name
        if type(value) != int:
            raise error_type(key, value, model, int)
        if value > 9999999999:  # 支持的最大时间戳
            raise ValueError(
                f"{key} value {value} must smaller than {model} support max value 9999999999.")

        return True
