from torm import Model
from torm import f


class User(Model):
    __config__ = "mysql"
    # __dbtype__ = "mysql"
    # __dbname__ = "test"
    # __tablename__ = "user"

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


# User.create_table()

user = User(name='kai', display_name='kai.he')
# user.create()
