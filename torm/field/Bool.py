from torm.field import Field
from torm.utl.Error import *


class Bool(Field):

    def __init__(self, *args, **kws):
        default = {
            'short': None,
            'long': None,
            'meta': 'short',
            'default': False,
            'field_type': 'bool',
            'key': False,
            'only_db_types': None
        }
        super().__init__(**default)

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if self.validate(value):
            self.value = value

    def validate(self, value):
        model = self.model
        key = self.name
        if type(value) != bool:
            raise error_type(key, value, model, bool)

        return True
