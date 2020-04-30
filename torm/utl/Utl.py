import re


def to_snake_name(hunp_str):
    ''' 驼峰形式字符串转成下划线形式 :param hunp_str: 驼峰形式字符串 :return: 字母全小写的下划线形式字符串 '''
    # 匹配正则，匹配小写字母和大写字母的分界位置
    p = re.compile(r'([a-z]|\d)([A-Z])')
    # 这里第二个参数使用了正则分组的后向引用
    sub = re.sub(p, r'\1_\2', hunp_str).lower()
    return sub


def to_up(x, all=True):
    s = x.group()
    if len(s) == 2:
        return x.group(1)[1].upper()
    elif len(s) == 1 and all:
        return x.group(0).upper()
    return x


def to_up(x, all=True):
    s = x.group()
    if len(s) == 2:
        return x.group(1)[1].upper()
    elif len(s) == 1 and all:
        return x.group(0).upper()
    return x


def to_camel_name(underline_str):
    ''' 下划线形式字符串转成大驼峰形式 :param underline_str: 下划线形式字符串 :return: 驼峰形式字符串 '''
    # 这里re.sub()函数第二个替换参数用到了一个匿名回调函数，回调函数的参数x为一个匹配对象，返回值为一个处理后的字符串
    # lambda x: x.group(1)[1].upper()
    sub = re.sub(r'(_\w)|(^\w)', to_up, underline_str)
    return sub


def to_small_camel_name(underline_str):
    ''' 下划线形式字符串转成小驼峰形式 :param underline_str: 下划线形式字符串 :return: 驼峰形式字符串 '''
    # 这里re.sub()函数第二个替换参数用到了一个匿名回调函数，回调函数的参数x为一个匹配对象，返回值为一个处理后的字符串
    # lambda x: x.group(1)[1].upper()
    sub = re.sub(r'(_\w)', to_up, underline_str)
    return sub
