from torm.field import Field
from torm.utl.Error import *


class Float(Field):

    def __init__(self, *args, **kws):
        default = {
            'left': None,
            'right': None,
            'meta': 'left',
            'default': 0,
            'field_type': 'decimal(12,6)',
            'key': False,
            'only_db_types': None
        }
        default.update(self.boundary(args))
        default.update(kws)

        _meta = ['left', 'right', 'both', 'neither']
        if default['meta'] not in _meta:
            raise ValueError('meta must be in %s.' % _meta)

        super().__init__(**default)

    def __get__(self, instance, owner):

        return self.value

    def __set__(self, instance, value):
        if self.validate(value):
            self.value = value
        else:
            raise ValidateError()

    # 边界条件
    def boundary(self, args):
        meta = 'left'
        boundary = {}
        if len(args) == 1:
            if type(args[0]) == list:
                boundary = dict(zip(['left', 'right'], args[0]))
                meta = 'both'
            elif type(args[0]) == tuple:
                boundary = dict(zip(['left', 'right'], args[0]))
                meta = 'neither'
            elif type(args[0]) == str:
                _p = args[0]
                _p = _p.strip(" ")
                boundary_type = _p[0] + _p[-1]
                numbers = _p.strip("[").strip(
                    "(").strip(")").strip("]").split(',')
                boundary = dict(zip(['left', 'right'], numbers))
                _metas = {'[)': 'left', '(]': 'right',
                          '[]': 'both', '()': 'neither'}
                meta = _metas[boundary_type]

            else:
                if meta == 'left':
                    boundary = dict(zip(['left'], args))
                if meta == 'right':
                    boundary = dict(zip(['right'], args))

        if len(args) == 2:
            boundary = dict(zip(['left', 'right'], args))
        boundary['meta'] = meta

        return boundary

    # 检查数据
    def validate(self, value):
        model = self.model
        key = self.name

        if not type(value) in [int, float]:
            raise error_type(key, value, model, [int, float])

        if self.left:
            if self.meta in ['both', 'left']:
                if not value >= self.left:
                    raise error_gt(key, value, model, self.left)

            if self.meta in ['neither', 'right']:
                if not value > self.right:
                    raise error_g(key, value, model, self.left)
        if self.right:
            if self.meta in ['both', 'right']:
                if not value <= self.right:
                    raise error_lt(key, value, model, self.right)

            if self.meta in ['neither', 'left']:
                if not value < self.right:
                    raise error_l(key, value, model, self.right)
