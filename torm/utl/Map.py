from collections.abc import Iterable
import inspect


def get_var_name(var, depth=2):
    # 当前命名空间
    fr = inspect.currentframe()
    for i in range(depth):
        fr = fr.f_back  # f_back获取父空间
    vars = fr.f_locals.items()  # 获取该命名空间的所有变量
    for var_name, var_val in vars:
        if var_val is var:  # 如果该变量的和var相同，则var_name就是var的变量名
            return var_name
    return None


class Map(dict):
    ###
    # js风格的dict,可以用["key"]或.key访问元素
    # python的dict,原有的属性除了魔法属性，还有：
    # 'clear', 'copy', 'fromkeys', 'get', 'items', 'keys',
    # 'pop', 'popitem', 'setdefault', 'update', 'values'
    # Map应该避免用.key访问以上同名的元素，这种情况可以用["key"]的方式访问
    ###

    def __init__(self, *args, _depth=2, **kwargs):
        for arg in args:
            if arg == None:
                continue
            if type(arg) == str:
                self[get_var_name(arg, _depth)] = arg
            elif type(arg) == set:
                for e in arg:
                    self[get_var_name(e, _depth)] = e
            elif isinstance(arg, Iterable):
                super().__init__(arg)
            else:
                self[get_var_name(arg, _depth)] = arg
        super().__init__(kwargs)

    def origin_method(self):
        return ['clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values']

    def __getattribute__(self, name):
        try:
            # 原有字典有该属性时，直接返回属性
            return super().__getattribute__(name)
        except AttributeError:
            try:  # 原有字典没有该属性时，尝试查找字典的key
                return self[name]
            except KeyError:  # 如果还找不到，返回None
                return None

    def __setattr__(self, name, value):
        if name == "origin_method":
            raise KeyError(f'Should not overlap Map origin method "{name}"')
        if name in self.origin_method():
            raise KeyError(f'Should not overlap Map origin method "{name}"')
        try:  # 原有字典有该属性时，将值绑定到该属性
            _value = super().__getattribute__(name)
            super().__setattr__(name, value)
        except AttributeError:  # 原有字典没有该属性时，将该属性作为字典的key，将值存入字典
            self[name] = value

    def pretty(self):
        values = ', '.join('\n    {} = {!r}'.format(
            i, self[i]) for i in self.keys())
        return '{}({}\n)'.format(self.__class__.__name__, values)


if __name__ == "__main__":
    a = {'a': 3, 'b': {'c': 4}}
    m = Map(a)
    print(m.pretty())
