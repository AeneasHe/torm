import decimal
import json


class Dict(dict):
    def __init__(self, *args, **kws):
        d = args[0]
        if d is not None:
            for k, v in d.items():
                self[k] = str(v) if isinstance(v, decimal.Decimal) else v
        return super().__init__()

    def __key(self, key):
        return "" if key is None else key.lower()

    def __setattr__(self, key, value):
        self[self.__key(key)] = value

    def __getattr__(self, key):
        return self.get(self.__key(key))

    def __getitem__(self, key):
        return super().get(self.__key(key))

    def __setitem__(self, key, value):
        return super().__setitem__(self.__key(key), value)

    def to_json(self):
        return json.dumps(self)

    def from_json(self, json_str):
        return json.loads(json_str)
