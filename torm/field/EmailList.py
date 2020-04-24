from torm.field import Field
from torm.utl.Error import *

import re


class EmailList(Field):
    def __init__(self, *args, **kwargs):
        default = {
            'left': None,
            'right': None,
            'meta': 'left',
            'default': [],
            'field_type': 'list',
            'key': False,
            'only_db_types': ['mongo']
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
        if type(value) != list:
            raise error_type(key, value, model, list)
        self.generator_check(value)
        return True

    def generator_check(self, g):
        for item in g:
            self.check(item)
            yield item

    def check(self, item):
        model = self.model
        key = self.name

        if type(item) != str:
            raise error_type(key, item, model, str)
        p = re.compile(r'''(
            [a-zA-Z0-9._%+-]+           # email-username
            @
            [a-zA-Z0-9.-]+              # domain-name
            \.[a-zA-Z]{2,4}             # dot-something
            )''', re.VERBOSE)

        s = re.search(p, item)
        if s:
            position = s.span()         # 第一个匹配的起始位置
            if len(item) == position[1]:
                return True
        raise error_type(key, item, model, "email")
