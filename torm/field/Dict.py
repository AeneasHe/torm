from torm.field import Field
from torm.utl.Error import *
import json


class Dict(Field):
    def __init__(self, *args, **kws):
        default = {
            'left': None,
            'right': None,
            'meta': 'left',
            'default': {},
            'field_type': 'dict',
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
        if type(value) != dict:
            raise error_type(key, value, model, dict)
        return True

    def to_json(self):
        return json.dumps(self.value)

    def from_json(self, json_str):
        self.value = json.loads(json_str)
        return self
