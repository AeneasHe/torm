import wpath
from torm import Model
from torm import f


class User(Model):
    __config__ = "mysql"

    id = f.Int(key=True)
    display_name = f.Str(32)
    name = f.Str(32)
    role = f.Str(64, default="user")

    phone = f.Str(32)
    email = f.Str(64)
    password = f.Str(64)

    register_finish_step = f.Int(default=1)
    verify_code = f.Str(6)
    verify_code_timestamp = f.Int()
    current_address = f.Str(42)

    login_timestamp = f.Int()
    create_at = f.Int()  # 创建时间


def test_create_table():
    User.create_table()


def test_insert_one():
    user = User(name='user_name', display_name='user name')
    user.display_name = 'User Name'
    u = User.InsertOne(user)
    print(u)


def test_find_one():
    r = User.FindOne()
    print(r)


def test_find_many():
    r = User.FindMany({'name': 'user_name'})
    print(r)


def test_update_one():
    r = User.UpdateOne({'name': 'user_name'}, {'display_name': 'User Name'})
    print(r)


def test_delete_one():
    r = User.DeleteOne({'name': 'user_name'})
    print(r)


# test_insert_one()
test_find_one()
# test_update_one()
# test_find_one()
# test_delete_one()
