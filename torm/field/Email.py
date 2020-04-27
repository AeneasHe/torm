from torm.field import Field
from torm.utl.Error import *

import re


class Email(Field):

    def __init__(self, *args, **kws):
        default = {
            'short': None,
            'long': None,
            'meta': 'short',
            'default': '',
            'field_type': 'email',
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
        if value == "":
            return True

        if type(value) != str:
            raise error_type(key, value, model, str)
        p = re.compile(r'''(
            [a-zA-Z0-9._%+-]+           # email-username
            @
            [a-zA-Z0-9.-]+              # domain-name
            \.[a-zA-Z]{2,4}             # dot-something
            )''', re.VERBOSE)

        s = re.search(p, value)
        if s:
            position = s.span()         # 第一个匹配的起始位置
            if len(value) == position[1]:
                return True
        raise error_type(key, value, model, "email")
