class BaseError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __bool__(self):
        return False


class TypeError(BaseError, TypeError):
    pass


class ValueError(BaseError, ValueError):
    pass


class ValidateError(BaseError):
    pass


class ConnectionError(BaseError):
    pass


def error_type(key, value, model, _type):
    if type(value) == str:
        value = '\'%s\'' % value
    return TypeError(
        'invalid type of %s, %s.%s value must be %s type.' % (value, model, key, _type))


def error_gt(key, value, model, limit):
    return ValueError(
        'invalid %s=%s, %s.%s must great than or equal to %s.' % (key, value, model, key, limit))


def error_g(key, value, model, limit):
    return ValueError(
        'invalid %s=%s, %s.%s must great than %s.' % (key, value, model, key, limit))


def error_lt(key, value, model, limit):
    return ValueError(
        'invalid %s=%s, %s.%s must smaller than or equal to %s.' % (key, value, model, key, limit))


def error_l(key, value, model, limit):
    return ValueError(
        'invalid %s=%s, %s.%s value must smaller than %s.' % (key, value, model, key, limit))
