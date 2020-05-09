import wpath
from torm import Model
from torm import f


class Group(Model):
    __tablename__ = 'group'  # 指定表名，默认采用类名的小写作为表名

    group = f.EmailList()
    group_hash = f.Str()
    display_name = f.Str()

    update_at = f.Timestamp()
    create_at = f.Timestamp()


user_email = 'thhk06@163.com'
groups = Group.FindMany({"group": user_email})
print(groups)
