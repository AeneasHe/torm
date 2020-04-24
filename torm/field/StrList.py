from torm.field import Field
from torm.utl.Error import *


class StrList(Field):
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

        # if len(args):
        #     args = (generator_check(args[0]),)

        # super().__init__(*args, **kwargs)

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

    def check(self, item):
        if not type(item) == str:
            raise TypeError('element require str type')

    def generator_check(self, g):
        for item in g:
            self.check(item)
            yield item
