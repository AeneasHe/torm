class Field(object):

    def __init__(self, *args, **kws):
        self.value = kws.get('default')  # 当前值
        self.default = kws.get('default')  # 默认值
        self.field_type = kws.get('field_type')  # 数据类型

        self.key = kws.get('key')  # 字段是否是key键

        self.left = kws.get('left')  # 最小值
        self.right = kws.get('right')  # 最大值
        self.meta = kws.get('meta')  # 边界判断规则

        self.only_db_types = kws.get('only_db_types', [])

    def __str__(self):
        return f'<{self.__class__.__name__} value={self.value}>'

    def __delete__(self, instance):
        raise AttributeError(r"%s attribute '%s' is forbidden to be deleted." % (
            instance.__class__.__name__, self.name))

    def __set_name__(self, owner, name):
        self.model = owner.__name__
        self.name = name
