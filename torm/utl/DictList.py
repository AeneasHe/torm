
from .Dict import Dict


def check(item):
    if not type(item) == dict:
        raise TypeError('element require dict type')


def generator_check(g):
    for item in g:
        check(item)
        yield item


class DictList(list):
    def __init__(self, *args, **kwargs):
        if len(args):
            args = (generator_check(args[0]),)

        super().__init__(*args, **kwargs)

    def __getitem__(self, index):
        return super().__getitem__(index)

    def __setitem__(self, key, item):
        check(item)
        return super().__setitem__(key, item)

    def append(self, item):
        check(item)
        super().append(item)

    def insert(self, item):
        check(item)
        super().append(item)
