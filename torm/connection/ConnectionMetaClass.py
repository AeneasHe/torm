import collections


class ConnectionMetaclass(type):

    @classmethod
    def __prepare__(cls, name, bases, **kws):
        return collections.OrderedDict()

    def __new__(cls, name, bases, attrs):
        if name == 'Connection':
            return type.__new__(cls, name, bases, attrs)

        return type.__new__(cls, name, bases, attrs)
