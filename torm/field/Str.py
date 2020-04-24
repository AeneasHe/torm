from torm.field import Field
from torm.utl.Error import *


class Str(Field):

    def __init__(self, *args, **kws):
        default = {
            'short': None,
            'long': None,
            'meta': 'short',
            'default': '',
            'field_type': 'varchar(32)',
            'key': False
        }
        default.update(kws)
        super(Str, self).__init__(**default)

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if self.validate(value):
            self.value = value

    def validate(self, value):
        model = self.model
        key = self.name
        if type(value) != str:
            raise error_type(key, value, model, str)

        return True
