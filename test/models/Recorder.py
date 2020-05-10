import wpath
from torm import Model
from torm import f


class Recorder(Model):
    __config__ = 'mysql'

    id = f.Int()
    name = f.Str()
    user = f.Str()
    password = f.Str()
    level = f.Int()

    update_at = f.Timestamp()
    create_at = f.Timestamp()


def test_find_many():
    rs = Recorder.count()
    print(rs)
    # for r in rs:
    #     print(r)


test_find_many()
