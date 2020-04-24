from functools import wraps
from flask import Flask, request, views, jsonify


def parse_field(fields={}):

    default = {
        int: [int, 'optional', 0],
        str: [str, 'optional', ''],
        float: [float, 'optional', 0],
        bool: [bool, 'optional', False]
    }
    _fields = {}
    for k in fields:
        v = fields[k]
        if type(v) in (list, tuple):
            if len(v) == 3:
                _fields[k] = list(v)
            if len(v) == 1:
                _fields[k] = default[v[0]]
            if len(v) == 2:
                _fields[k] = list(v) + default[v[0]][2]
        else:
            _fields[k] = default[v]

    return _fields


def parse_form(form, fields={}):
    form = dict(form)
    _form = {}
    _errors = []
    for k in fields:
        if fields[k][1] == 'required':
            value = form.get(k)
            if value == None:
                _errors.append(ValueError(f"{k} required"))
                continue
        else:
            value = form.get(k, fields[k][2])
        try:
            value = fields[k][0](value)
        except:
            _errors.append(
                TypeError(f"{k} require {str(fields[k][0].__name__)} type value"))
            continue
        _form[k] = value
    if len(_errors):
        raise Exception("; ".join([str(e) for e in _errors]) + ".")
    return _form


def rsp_error(msg="error", data=[], code=400):
    return jsonify({'code': code, 'msg': str(msg), 'data': data})


def rsp_success(msg="success", data=[], code=200):
    return jsonify({'code': code, 'msg': str(msg), 'data': data})


def validate(fields={}, **kws):
    fields = parse_field(fields)

    def outter(handler):
        @wraps(handler)
        def wrapper(*args, **kws):
            if request.method == "GET":
                form = request.args
            else:
                if request.form:
                    form = request.form
                else:
                    form = request.get_json()
            try:
                form = parse_form(form, fields)
            except Exception as e:
                return rsp_error(msg=e)

            return handler(*args, **kws)
        return wrapper
    return outter


def validate_doc(handler):
    @wraps(handler)
    def wrapper(*args, **kws):
        doc = handler.__doc__

        doc = doc.replace(' ', '').strip('\n').split('\n')
        _field = [line.strip(' ').split(':') for line in doc]
        field = {}
        for f in _field:
            field[f[0]] = f[1]

        return handler(*args, **kws)
    return wrapper
